import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.models.user import User
from app.permissions import (
    ALL_PERMISSIONS, ENFORCE_PERMISSIONS, PERMISSION_LABELS, WILDCARD,
)

settings   = get_settings()
pwd_ctx    = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer     = HTTPBearer(auto_error=False)


# ── Password ──────────────────────────────────────────────────────────────
def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


# ── JWT ───────────────────────────────────────────────────────────────────
def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None


# ── FastAPI dependencies ──────────────────────────────────────────────────
def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


# ── Phân quyền ────────────────────────────────────────────────────────────
def user_permissions(user: User) -> set[str]:
    """
    Quyền thực tế của một tài khoản. Chỉ tài khoản admin có vai trò mới có
    quyền; vai trò lưu ["*"] nghĩa là toàn quyền.
    """
    if not (user.is_admin and user.role_id):
        return set()
    role = user.role
    try:
        codes = json.loads(role.permissions) if role.permissions else []
    except (json.JSONDecodeError, TypeError):
        codes = []
    if WILDCARD in codes:
        return set(ALL_PERMISSIONS)
    return {c for c in codes if c in PERMISSION_LABELS}


def has_permission(user: User, *codes: str) -> bool:
    """True nếu tài khoản có ÍT NHẤT MỘT trong các quyền truyền vào."""
    granted = user_permissions(user)
    return any(code in granted for code in codes)


def require(*codes: str):
    """
    Khai báo quyền của một endpoint — truyền nhiều mã nghĩa là chỉ cần có một
    trong số đó (VD upload ảnh: sửa sản phẩm HOẶC sửa bài viết).

        @router.post("/", dependencies=[Depends(require("products.create"))])

    Khi ENFORCE_PERMISSIONS = False (mặc định hiện tại), hàm này chỉ yêu cầu
    đăng nhập bằng tài khoản admin — phân quyền chỉ dùng để ẩn/hiện giao diện,
    gọi thẳng API thì admin nào cũng làm được. Bật cờ đó lên là mọi endpoint
    kiểm tra quyền thật, không phải sửa thêm chỗ nào.
    """
    if not ENFORCE_PERMISSIONS:
        return get_current_admin

    def dependency(user: User = Depends(get_current_admin)) -> User:
        if not has_permission(user, *codes):
            labels = ", ".join(PERMISSION_LABELS.get(c, c) for c in codes)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tài khoản của bạn không có quyền: {labels}.",
            )
        return user
    return dependency


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> Optional[User]:
    """Non-throwing – returns None if not authenticated."""
    if not credentials:
        return None
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        return None
    try:
        user = User.get_by_id(user_id)
        return user if user.is_active else None
    except User.DoesNotExist:
        return None
