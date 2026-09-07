from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegister(BaseModel):
    email:     EmailStr
    full_name: Optional[str] = None
    password:  str
    phone:     Optional[str] = None

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone:     Optional[str] = None
    address:   Optional[str] = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:        int
    email:     str
    full_name: Optional[str] = None
    phone:     Optional[str] = None
    address:   Optional[str] = None
    is_active: bool
    is_admin:  bool
    created_at: datetime
    # Phân quyền trang admin — rỗng với tài khoản khách
    role_id:     Optional[int] = None
    role_name:   Optional[str] = None
    permissions: list[str] = []

class TokenOut(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserOut


def user_out(user) -> UserOut:
    """
    UserOut kèm vai trò và danh sách quyền đã tính sẵn — trang admin dùng để
    ẩn/hiện tab và nút, không phải gọi thêm API.
    """
    from app.auth import user_permissions          # tránh vòng import lúc nạp module
    from app.permissions import ALL_PERMISSIONS

    out = UserOut.model_validate(user, from_attributes=True)
    role = user.role if getattr(user, "role_id", None) else None
    granted = user_permissions(user)
    out.role_name   = role.name if role else None
    out.permissions = [code for code in ALL_PERMISSIONS if code in granted]
    return out
