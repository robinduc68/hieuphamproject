from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from peewee import DoesNotExist, IntegrityError

from app.models.order import Order, OrderItem
from app.models.newsletter import NewsletterSubscription as Newsletter
from app.models.product import Product, ProductSize
from app.models.user import User
from app.schemas.order import (
    OrderCreate, OrderOut, OrderItemOut,
    OrderStatusUpdate, NewsletterSubscribe, NewsletterOut,
)
from app.auth import get_current_user, get_current_admin, get_optional_user
from app.database import get_db

router      = APIRouter(prefix="/api/orders",     tags=["Orders"])
nl_router   = APIRouter(prefix="/api/newsletter", tags=["Newsletter"])


# ── helpers ───────────────────────────────────────────────────────────────
def _order_to_out(order: Order) -> OrderOut:
    items = list(OrderItem.select().where(OrderItem.order == order))
    return OrderOut(
        id=order.id,
        email=order.email,
        full_name=order.full_name,
        phone=order.phone,
        address=order.address,
        city=order.city,
        country=order.country,
        note=order.note,
        total=Decimal(str(order.total)),
        status=order.status,
        tracking_code=order.tracking_code,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                id=i.id,
                product_id=i.product_id,
                size=i.size,
                quantity=i.quantity,
                price=Decimal(str(i.price)),
            )
            for i in items
        ],
    )


# ══════════════════════════════════════════════════════════════════════════
# ORDER endpoints
# ══════════════════════════════════════════════════════════════════════════
@router.post("/", response_model=OrderOut, status_code=201)
def create_order(
    data:         OrderCreate,
    current_user: Optional[User] = Depends(get_optional_user),
    _db=Depends(get_db),
):
    # Validate all items & compute total
    line_items = []
    total = Decimal("0")
    for item in data.items:
        try:
            product = Product.get(Product.id == item.product_id, Product.is_active == True)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Sản phẩm #{item.product_id} không tồn tại.")

        # Check size availability
        try:
            sz = ProductSize.get(
                ProductSize.product == product,
                ProductSize.size == item.size,
                ProductSize.is_available == True,
            )
        except DoesNotExist:
            raise HTTPException(
                status_code=400,
                detail=f"Size {item.size} của '{product.name}' hiện không có hàng.",
            )

        line_price = Decimal(str(product.price)) * item.quantity
        total += line_price
        line_items.append((product, item.size, item.quantity, Decimal(str(product.price))))

    with _db.atomic():
        order = Order.create(
            user=current_user,
            email=data.email,
            full_name=data.full_name,
            phone=data.phone,
            address=data.address,
            city=data.city,
            country=data.country,
            note=data.note,
            total=total,
            status="pending",
        )
        for product, size, qty, price in line_items:
            OrderItem.create(
                order=order,
                product=product,
                size=size,
                quantity=qty,
                price=price,
            )

    return _order_to_out(order)


@router.get("/my-orders", response_model=list[OrderOut])
def my_orders(
    current_user: User = Depends(get_current_user),
    _db=Depends(get_db),
):
    orders = (
        Order.select()
        .where(Order.user == current_user)
        .order_by(Order.created_at.desc())
    )
    return [_order_to_out(o) for o in orders]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id:     int,
    current_user: Optional[User] = Depends(get_optional_user),
    _db=Depends(get_db),
):
    try:
        order = Order.get_by_id(order_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại.")

    # Only owner or admin can view
    if current_user is None or (not current_user.is_admin and order.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Không có quyền truy cập đơn hàng này.")

    return _order_to_out(order)


# ── Admin: list all orders ────────────────────────────────────────────────
@router.get("/", response_model=list[OrderOut], dependencies=[Depends(get_current_admin)])
def list_all_orders(
    status:   Optional[str] = Query(None),
    page:     int           = Query(1, ge=1),
    per_page: int           = Query(20, ge=1, le=100),
    _db=Depends(get_db),
):
    qs = Order.select().order_by(Order.created_at.desc())
    if status:
        qs = qs.where(Order.status == status)
    orders = list(qs.offset((page - 1) * per_page).limit(per_page))
    return [_order_to_out(o) for o in orders]


@router.patch("/{order_id}/status", response_model=OrderOut,
              dependencies=[Depends(get_current_admin)])
def update_order_status(order_id: int, data: OrderStatusUpdate, _db=Depends(get_db)):
    try:
        order = Order.get_by_id(order_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại.")
    order.status = data.status
    if data.tracking_code:
        order.tracking_code = data.tracking_code
    order.save()
    return _order_to_out(order)


# ══════════════════════════════════════════════════════════════════════════
# NEWSLETTER
# ══════════════════════════════════════════════════════════════════════════
@nl_router.post("/subscribe", response_model=NewsletterOut, status_code=201)
def subscribe(data: NewsletterSubscribe, _db=Depends(get_db)):
    try:
        sub = Newsletter.get(Newsletter.email == data.email)
        if not sub.is_active:
            sub.is_active = True
            if data.full_name:
                sub.full_name = data.full_name
            sub.save()
        return NewsletterOut.model_validate(sub, from_attributes=True)
    except DoesNotExist:
        sub = Newsletter.create(email=data.email, full_name=data.full_name)
        return NewsletterOut.model_validate(sub, from_attributes=True)


@nl_router.delete("/unsubscribe/{email}", status_code=204)
def unsubscribe(email: str, _db=Depends(get_db)):
    try:
        sub = Newsletter.get(Newsletter.email == email)
        sub.is_active = False
        sub.save()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Email không tồn tại trong danh sách.")
