from peewee import (
    CharField, TextField, DecimalField,
    IntegerField, ForeignKeyField
)
from .base import BaseModel
from .user import User
from .product import Product, ProductSize


class Order(BaseModel):
    STATUS_CHOICES = (
        ("pending",    "Chờ xác nhận"),
        ("confirmed",  "Đã xác nhận"),
        ("processing", "Đang xử lý"),
        ("shipped",    "Đang giao"),
        ("delivered",  "Đã giao"),
        ("cancelled",  "Đã huỷ"),
        ("refunded",   "Đã hoàn tiền"),
    )

    user             = ForeignKeyField(User, backref="orders", null=True, on_delete="SET NULL")
    # Guest checkout fields
    guest_name       = CharField(max_length=255, null=True)
    guest_email      = CharField(max_length=255, null=True)
    guest_phone      = CharField(max_length=30,  null=True)

    shipping_address = TextField()
    status           = CharField(max_length=30, default="pending")
    total_amount     = DecimalField(max_digits=14, decimal_places=0)
    note             = TextField(null=True)

    class Meta:
        table_name = "orders"


class OrderItem(BaseModel):
    order         = ForeignKeyField(Order, backref="items", on_delete="CASCADE")
    product       = ForeignKeyField(Product, backref="order_items", on_delete="RESTRICT")
    product_size  = ForeignKeyField(ProductSize, backref="order_items", null=True, on_delete="SET NULL")
    size_label    = CharField(max_length=20)          # snapshot tại thời điểm đặt
    product_name  = CharField(max_length=255)         # snapshot
    unit_price    = DecimalField(max_digits=14, decimal_places=0)
    quantity      = IntegerField(default=1)
    subtotal      = DecimalField(max_digits=14, decimal_places=0)

    class Meta:
        table_name = "order_items"
