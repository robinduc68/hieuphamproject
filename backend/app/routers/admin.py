import json
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, ConfigDict, EmailStr
from peewee import DoesNotExist, fn

from app.models.user import User
from app.models.role import Role
from app.permissions import PERMISSION_GROUPS, WILDCARD, clean_permissions
from app.models.order import Order
from app.models.product import Product
from app.schemas.user import UserOut, user_out
from app.auth import get_current_admin, hash_password, require, user_permissions
from app.database import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ── Schemas ───────────────────────────────────────────────────────────────
class StatsOut(BaseModel):
    total_orders:   int
    total_revenue:  Decimal
    total_products: int
    total_users:    int


class AdminUserCreate(BaseModel):
    email:     EmailStr
    password:  str
    full_name: Optional[str] = None
    phone:     Optional[str] = None
    is_admin:  bool = False
    is_active: bool = True
    role_id:   Optional[int] = None


class RoleIn(BaseModel):
    name:        str
    description: Optional[str] = None
    permissions: list[str] = []


class AdminUserUpdate(BaseModel):
    full_name: Optional[str]  = None
    email:     Optional[str]  = None
    phone:     Optional[str]  = None
    is_admin:  Optional[bool] = None
    is_active: Optional[bool] = None
    password:  Optional[str]  = None
    role_id:   Optional[int]  = None


MIN_PASSWORD_LEN = 6


def _check_password(password: str) -> None:
    if len(password or "") < MIN_PASSWORD_LEN:
        raise HTTPException(
            status_code=400,
            detail=f"Mật khẩu phải có ít nhất {MIN_PASSWORD_LEN} ký tự.",
        )


def _resolve_role(role_id: Optional[int], is_admin: bool) -> Optional[Role]:
    """
    Tài khoản admin bắt buộc có vai trò, nếu không sẽ vào được trang quản trị
    mà không thao tác được gì. Tài khoản khách thì không cần vai trò.
    """
    if not is_admin:
        return None
    if not role_id:
        raise HTTPException(
            status_code=400,
            detail="Tài khoản admin phải được gán một vai trò để biết được làm những gì.",
        )
    role = Role.get_or_none(Role.id == role_id)
    if role is None:
        raise HTTPException(status_code=400, detail="Vai trò không tồn tại.")
    return role


def _role_out(role: Role) -> dict:
    try:
        permissions = json.loads(role.permissions) if role.permissions else []
    except (json.JSONDecodeError, TypeError):
        permissions = []
    return {
        "id":          role.id,
        "name":        role.name,
        "description": role.description,
        "permissions": permissions,
        "is_system":   role.is_system,
        "user_count":  User.select().where(User.role == role.id).count(),
    }


def _check_email_free(email: str, exclude_id: Optional[int] = None) -> None:
    qs = User.select().where(fn.LOWER(User.email) == email.lower())
    if exclude_id is not None:
        qs = qs.where(User.id != exclude_id)
    if qs.exists():
        raise HTTPException(status_code=409, detail=f"Email '{email}' đã được dùng cho tài khoản khác.")


class PaginatedUsers(BaseModel):
    total:    int
    page:     int
    per_page: int
    results:  list[UserOut]


# ── Stats ─────────────────────────────────────────────────────────────────
@router.get("/stats", response_model=StatsOut, dependencies=[Depends(require("dashboard.view"))])
def get_stats(_db=Depends(get_db)):
    total_orders   = Order.select().count()
    revenue_row    = Order.select(fn.COALESCE(fn.SUM(Order.total), 0)).scalar()
    total_revenue  = Decimal(str(revenue_row or 0))
    total_products = Product.select().where(Product.is_active == True).count()
    total_users    = User.select().where(User.is_active == True).count()
    return StatsOut(
        total_orders=total_orders,
        total_revenue=total_revenue,
        total_products=total_products,
        total_users=total_users,
    )


# ── Users ─────────────────────────────────────────────────────────────────
@router.get("/users", response_model=PaginatedUsers, dependencies=[Depends(require("users.view"))])
def list_users(
    page:     int            = Query(1, ge=1),
    per_page: int            = Query(20, ge=1, le=100),
    search:   Optional[str]  = Query(None),
    is_admin: Optional[bool] = Query(None),
    _db=Depends(get_db),
):
    qs = User.select().order_by(User.created_at.desc())
    if search:
        qs = qs.where(
            fn.LOWER(User.email).contains(search.lower()) |
            fn.LOWER(fn.COALESCE(User.full_name, "")).contains(search.lower())
        )
    if is_admin is not None:
        qs = qs.where(User.is_admin == is_admin)
    total = qs.count()
    users = list(qs.offset((page - 1) * per_page).limit(per_page))
    return PaginatedUsers(
        total=total,
        page=page,
        per_page=per_page,
        results=[user_out(u) for u in users],
    )


@router.post("/users", response_model=UserOut, status_code=201,
             dependencies=[Depends(require("users.create"))])
def create_user(data: AdminUserCreate, _db=Depends(get_db)):
    _check_password(data.password)
    _check_email_free(data.email)
    role = _resolve_role(data.role_id, data.is_admin)
    user = User.create(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        phone=data.phone,
        is_admin=data.is_admin,
        is_active=data.is_active,
        role=role,
    )
    return user_out(user)


@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require("users.update"))])
def update_user(
    user_id: int,
    data: AdminUserUpdate,
    current_admin: User = Depends(get_current_admin),
    _db=Depends(get_db),
):
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    payload = data.model_dump(exclude_none=True)

    losing_admin  = payload.get("is_admin")  is False and user.is_admin
    losing_active = payload.get("is_active") is False and user.is_active

    # Tự khoá / tự hạ quyền mình là tự nhốt mình ngoài trang admin
    if user.id == current_admin.id:
        if losing_admin:
            raise HTTPException(status_code=400, detail="Không thể tự bỏ quyền admin của chính mình.")
        if losing_active:
            raise HTTPException(status_code=400, detail="Không thể tự khoá tài khoản của chính mình.")

    # is_admin không gửi lên thì giữ nguyên giá trị cũ khi kiểm tra vai trò
    will_be_admin = payload.get("is_admin", user.is_admin)
    if "role_id" in payload or "is_admin" in payload:
        payload["role"] = _resolve_role(payload.pop("role_id", user.role_id), will_be_admin)
    payload.pop("role_id", None)

    new_email = payload.get("email")
    if new_email and new_email.lower() != user.email.lower():
        _check_email_free(new_email, exclude_id=user.id)

    if "password" in payload:
        password = payload.pop("password")
        _check_password(password)
        user.hashed_password = hash_password(password)

    for field, val in payload.items():
        setattr(user, field, val)
    user.save()
    return user_out(user)


@router.delete("/users/{user_id}", status_code=204, dependencies=[Depends(require("users.delete"))])
def delete_user(user_id: int, current_admin: User = Depends(get_current_admin), _db=Depends(get_db)):
    """
    Xoá hẳn tài khoản. Đơn hàng cũ vẫn còn (Order.user là SET NULL và đã lưu sẵn
    tên/email/địa chỉ lúc đặt). Muốn giữ tài khoản mà chặn đăng nhập thì dùng
    is_active = false ở endpoint cập nhật.
    """
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Không thể xoá chính mình.")
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete_instance()


# ── Vai trò & phân quyền ──────────────────────────────────────────────────
@router.get("/permissions", dependencies=[Depends(require("roles.view"))])
def list_permissions():
    """Danh mục quyền để trang admin dựng bảng tick — xem app/permissions.py."""
    return [
        {
            "key":   group["key"],
            "label": group["label"],
            "permissions": [{"code": code, "label": label} for code, label in group["permissions"]],
        }
        for group in PERMISSION_GROUPS
    ]


@router.get("/roles", dependencies=[Depends(require("roles.view"))])
def list_roles(_db=Depends(get_db)):
    return [_role_out(r) for r in Role.select().order_by(Role.is_system.desc(), Role.name)]


@router.post("/roles", status_code=201, dependencies=[Depends(require("roles.manage"))])
def create_role(data: RoleIn, _db=Depends(get_db)):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên vai trò.")
    if Role.select().where(fn.LOWER(Role.name) == name.lower()).exists():
        raise HTTPException(status_code=409, detail=f"Đã có vai trò tên '{name}'.")
    role = Role.create(
        name=name,
        description=data.description,
        permissions=json.dumps(clean_permissions(data.permissions), ensure_ascii=False),
        is_system=False,
    )
    return _role_out(role)


@router.put("/roles/{role_id}", dependencies=[Depends(require("roles.manage"))])
def update_role(role_id: int, data: RoleIn, _db=Depends(get_db)):
    role = Role.get_or_none(Role.id == role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Vai trò không tồn tại.")

    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên vai trò.")
    if Role.select().where(fn.LOWER(Role.name) == name.lower(), Role.id != role.id).exists():
        raise HTTPException(status_code=409, detail=f"Đã có vai trò tên '{name}'.")

    role.name        = name
    role.description = data.description
    # Vai trò gốc luôn giữ toàn quyền — bỏ bớt quyền của nó là tự khoá đường vào
    if not role.is_system:
        role.permissions = json.dumps(clean_permissions(data.permissions), ensure_ascii=False)
    role.save()
    return _role_out(role)


@router.delete("/roles/{role_id}", status_code=204, dependencies=[Depends(require("roles.manage"))])
def delete_role(role_id: int, _db=Depends(get_db)):
    role = Role.get_or_none(Role.id == role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Vai trò không tồn tại.")
    if role.is_system:
        raise HTTPException(status_code=400, detail="Không thể xoá vai trò gốc của hệ thống.")
    in_use = User.select().where(User.role == role.id).count()
    if in_use:
        raise HTTPException(
            status_code=409,
            detail=f"Còn {in_use} tài khoản đang dùng vai trò này — hãy đổi vai trò cho họ trước.",
        )
    role.delete_instance()
