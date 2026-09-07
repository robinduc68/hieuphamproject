from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, ConfigDict, EmailStr
from peewee import DoesNotExist, fn

from app.models.user import User
from app.models.order import Order
from app.models.product import Product
from app.schemas.user import UserOut
from app.auth import get_current_admin, hash_password
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


class AdminUserUpdate(BaseModel):
    full_name: Optional[str]  = None
    email:     Optional[str]  = None
    phone:     Optional[str]  = None
    is_admin:  Optional[bool] = None
    is_active: Optional[bool] = None
    password:  Optional[str]  = None


MIN_PASSWORD_LEN = 6


def _check_password(password: str) -> None:
    if len(password or "") < MIN_PASSWORD_LEN:
        raise HTTPException(
            status_code=400,
            detail=f"Mật khẩu phải có ít nhất {MIN_PASSWORD_LEN} ký tự.",
        )


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
@router.get("/stats", response_model=StatsOut, dependencies=[Depends(get_current_admin)])
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
@router.get("/users", response_model=PaginatedUsers, dependencies=[Depends(get_current_admin)])
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
        results=[UserOut.model_validate(u, from_attributes=True) for u in users],
    )


@router.post("/users", response_model=UserOut, status_code=201,
             dependencies=[Depends(get_current_admin)])
def create_user(data: AdminUserCreate, _db=Depends(get_db)):
    _check_password(data.password)
    _check_email_free(data.email)
    user = User.create(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        phone=data.phone,
        is_admin=data.is_admin,
        is_active=data.is_active,
    )
    return UserOut.model_validate(user, from_attributes=True)


@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(get_current_admin)])
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
    return UserOut.model_validate(user, from_attributes=True)


@router.delete("/users/{user_id}", status_code=204, dependencies=[Depends(get_current_admin)])
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
