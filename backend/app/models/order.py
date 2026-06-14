from peewee import (
    CharField, TextField, DecimalField,
    IntegerField, ForeignKeyField
)
from .base import BaseModel
from .user import User
from .product import Product


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
    PAYMENT_METHOD_CHOICES = (
        ("cod",           "Tiền mặt khi nhận"),
        ("bank_transfer", "Chuyển khoản"),
        ("vnpay",         "VNPay"),
        ("momo",          "MoMo"),
    )
    PAYMENT_STATUS_CHOICES = (
        ("unpaid",   "Chưa thanh toán"),
        ("paid",     "Đã thanh toán"),
        ("refunded", "Đã hoàn tiền"),
    )

    user             = ForeignKeyField(User, backref="orders", null=True, on_delete="SET NULL")
    email            = CharField(max_length=255)
    full_name        = CharField(max_length=200)
    phone            = CharField(max_length=20)
    address          = TextField()
    ward             = CharField(max_length=100, null=True)
    district         = CharField(max_length=100, null=True)
    city             = CharField(max_length=100)
    country          = CharField(max_length=100, default="Vietnam")
    note             = TextField(null=True)
    total            = DecimalField(max_digits=16, decimal_places=0)   # subtotal (sum of items)
    shipping_fee     = DecimalField(max_digits=16, decimal_places=0, default=0)
    discount_code    = CharField(max_length=50, null=True)
    discount_amount  = DecimalField(max_digits=16, decimal_places=0, default=0)
    grand_total      = DecimalField(max_digits=16, decimal_places=0)   # total + shipping - discount
    payment_method   = CharField(max_length=30, default="cod")
    payment_status   = CharField(max_length=20, default="unpaid")
    status           = CharField(max_length=20, default="pending")
    tracking_code    = CharField(max_length=100, null=True)

    class Meta:
        table_name = "orders"


class OrderItem(BaseModel):
    order            = ForeignKeyField(Order, backref="items", on_delete="CASCADE")
    product          = ForeignKeyField(Product, backref="order_items", null=True, on_delete="SET NULL")
    product_name     = CharField(max_length=255, null=True)   # snapshot
    size             = CharField(max_length=20)
    quantity         = IntegerField(default=1)
    price            = DecimalField(max_digits=14, decimal_places=0)   # unit price snapshot (incl. adjustments)
    tailoring_method = CharField(max_length=60, null=True)   # option_key snapshot
    lining_type      = CharField(max_length=60, null=True)
    color_option     = CharField(max_length=60, null=True)

    class Meta:
        table_name = "order_items"
