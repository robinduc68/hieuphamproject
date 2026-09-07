from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from peewee import DoesNotExist, IntegrityError

from app.models.order import Order, OrderItem
from app.models.newsletter import NewsletterSubscription as Newsletter
from app.models.product import Product, ProductSize
from app.models.customization import CustomizationOption
from app.models.user import User
from app.schemas.order import (
    OrderCreate, OrderOut, OrderItemOut,
    OrderStatusUpdate, NewsletterSubscribe, NewsletterOut,
    PaginatedOrders,
)
from app.auth import get_current_user, get_optional_user, require
from app.database import get_db

router    = APIRouter(prefix="/api/orders",     tags=["Orders"])
nl_router = APIRouter(prefix="/api/newsletter", tags=["Newsletter"])


# ── helpers ───────────────────────────────────────────────────────────────
def _item_to_out(i: OrderItem) -> OrderItemOut:
    return OrderItemOut(
        id=i.id,
        product_id=i.product_id,
        product_name=i.product_name,   # snapshot – no join needed
        size=i.size,
        quantity=i.quantity,
        price=Decimal(str(i.price)),
        tailoring_method=i.tailoring_method,
        lining_type=i.lining_type,
        color_option=i.color_option,
    )


def _order_to_out(order: Order) -> OrderOut:
    items = list(OrderItem.select().where(OrderItem.order == order))
    return OrderOut(
        id=order.id,
        email=order.email,
        full_name=order.full_name,
        phone=order.phone,
        address=order.address,
        ward=order.ward,
        district=order.district,
        city=order.city,
        country=order.country,
        note=order.note,
        total=Decimal(str(order.total)),
        shipping_fee=Decimal(str(order.shipping_fee)),
        discount_code=order.discount_code,
        discount_amount=Decimal(str(order.discount_amount)),
        grand_total=Decimal(str(order.grand_total)),
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        status=order.status,
        tracking_code=order.tracking_code,
        created_at=order.created_at,
        items=[_item_to_out(i) for i in items],
    )


def _get_adjustment(group_key: str, option_key: Optional[str]) -> Decimal:
    """Look up price_adjustment for a customization option; return 0 if not found."""
    if not option_key:
        return Decimal("0")
    try:
        opt = CustomizationOption.get(
            CustomizationOption.group_key == group_key,
            CustomizationOption.option_key == option_key,
            CustomizationOption.is_active == True,
        )
        return Decimal(str(opt.price_adjustment))
    except DoesNotExist:
        return Decimal("0")


# ══════════════════════════════════════════════════════════════════════════
# ORDER endpoints
# ══════════════════════════════════════════════════════════════════════════
@router.post("/", response_model=OrderOut, status_code=201)
def create_order(
    data:         OrderCreate,
    current_user: Optional[User] = Depends(get_optional_user),
    _db=Depends(get_db),
):
    line_items = []
    total = Decimal("0")

    for item in data.items:
        try:
            product = Product.get(Product.id == item.product_id, Product.is_active == True)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Sản phẩm #{item.product_id} không tồn tại.")

        # Size validation: skip for custom tailoring
        if item.tailoring_method != "custom":
            size_to_check = item.size
            try:
                ProductSize.get(
                    ProductSize.product == product,
                    ProductSize.size == size_to_check,
                    ProductSize.is_available == True,
                )
            except DoesNotExist:
                raise HTTPException(
                    status_code=400,
                    detail=f"Size {item.size} của '{product.name}' hiện không có hàng.",
                )

        # Compute unit price: base + customization adjustments
        adj = (
            _get_adjustment("tailoring_method", item.tailoring_method)
            + _get_adjustment("lining_type",      item.lining_type)
            + _get_adjustment("color_option",      item.color_option)
        )
        unit_price = Decimal(str(product.price)) + adj
        line_total = unit_price * item.quantity
        total += line_total

        line_items.append({
            "product":          product,
            "product_name":     product.name,
            "size":             item.size,
            "quantity":         item.quantity,
            "price":            unit_price,
            "tailoring_method": item.tailoring_method,
            "lining_type":      item.lining_type,
            "color_option":     item.color_option,
        })

    shipping_fee    = Decimal("0")   # free shipping (extend later)
    discount_amount = Decimal("0")
    grand_total     = total + shipping_fee - discount_amount

    with _db.atomic():
        order = Order.create(
            user=current_user,
            email=data.email,
            full_name=data.full_name,
            phone=data.phone,
            address=data.address,
            ward=data.ward,
            district=data.district,
            city=data.city,
            country=data.country,
            note=data.note,
            total=total,
            shipping_fee=shipping_fee,
            discount_amount=discount_amount,
            grand_total=grand_total,
            payment_method=data.payment_method,
            payment_status="unpaid",
            status="pending",
        )
        for li in line_items:
            OrderItem.create(
                order=order,
                product=li["product"],
                product_name=li["product_name"],
                size=li["size"],
                quantity=li["quantity"],
                price=li["price"],
                tailoring_method=li["tailoring_method"],
                lining_type=li["lining_type"],
                color_option=li["color_option"],
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

    if current_user is None or (not current_user.is_admin and order.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Không có quyền truy cập đơn hàng này.")

    return _order_to_out(order)


# ── Admin: list all orders (paginated) ───────────────────────────────────
@router.get("/", response_model=PaginatedOrders, dependencies=[Depends(require("orders.view"))])
def list_all_orders(
    status:         Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    page:           int           = Query(1, ge=1),
    per_page:       int           = Query(20, ge=1, le=100),
    _db=Depends(get_db),
):
    qs = Order.select().order_by(Order.created_at.desc())
    if status:
        qs = qs.where(Order.status == status)
    if payment_status:
        qs = qs.where(Order.payment_status == payment_status)
    total  = qs.count()
    orders = list(qs.offset((page - 1) * per_page).limit(per_page))
    return PaginatedOrders(
        total=total,
        page=page,
        per_page=per_page,
        results=[_order_to_out(o) for o in orders],
    )


@router.patch("/{order_id}/status", response_model=OrderOut,
              dependencies=[Depends(require("orders.update_status"))])
def update_order_status(order_id: int, data: OrderStatusUpdate, _db=Depends(get_db)):
    try:
        order = Order.get_by_id(order_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại.")
    order.status = data.status
    if data.tracking_code is not None:
        order.tracking_code = data.tracking_code
    if data.payment_status is not None:
        order.payment_status = data.payment_status
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
