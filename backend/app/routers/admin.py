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


class AdminUserUpdate(BaseModel):
    full_name: Optional[str]  = None
    email:     Optional[str]  = None
    phone:     Optional[str]  = None
    is_admin:  Optional[bool] = None
    is_active: Optional[bool] = None
    password:  Optional[str]  = None


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


@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(get_current_admin)])
def update_user(user_id: int, data: AdminUserUpdate, _db=Depends(get_db)):
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    payload = data.model_dump(exclude_none=True)
    if "password" in payload:
        user.hashed_password = hash_password(payload.pop("password"))
    for field, val in payload.items():
        setattr(user, field, val)
    user.save()
    return UserOut.model_validate(user, from_attributes=True)


@router.delete("/users/{user_id}", status_code=204, dependencies=[Depends(get_current_admin)])
def delete_user(user_id: int, current_admin: User = Depends(get_current_admin), _db=Depends(get_db)):
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Không thể xoá chính mình.")
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    user.save()
