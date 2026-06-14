from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class OrderItemIn(BaseModel):
    product_id:       int
    size:             str
    quantity:         int = 1
    tailoring_method: Optional[str] = None  # option_key, e.g. 'size' or 'custom'
    lining_type:      Optional[str] = None  # option_key, e.g. 'lien_ta' or 'yem_roi'
    color_option:     Optional[str] = None  # option_key, e.g. 'same' or 'custom_color'


class OrderCreate(BaseModel):
    email:          EmailStr
    full_name:      str
    phone:          str
    address:        str
    ward:           Optional[str] = None
    district:       Optional[str] = None
    city:           str
    country:        str = "Vietnam"
    payment_method: str = "cod"
    note:           Optional[str] = None
    items:          list[OrderItemIn]


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:               int
    product_id:       Optional[int] = None
    product_name:     Optional[str] = None
    size:             str
    quantity:         int
    price:            Decimal
    tailoring_method: Optional[str] = None
    lining_type:      Optional[str] = None
    color_option:     Optional[str] = None

    @field_validator("price", mode="before")
    @classmethod
    def coerce(cls, v): return Decimal(str(v))


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:              int
    email:           str
    full_name:       str
    phone:           str
    address:         str
    ward:            Optional[str] = None
    district:        Optional[str] = None
    city:            str
    country:         str
    note:            Optional[str] = None
    total:           Decimal
    shipping_fee:    Decimal
    discount_code:   Optional[str] = None
    discount_amount: Decimal
    grand_total:     Decimal
    payment_method:  str
    payment_status:  str
    status:          str
    tracking_code:   Optional[str] = None
    items:           list[OrderItemOut] = []
    created_at:      datetime

    @field_validator("total", "shipping_fee", "discount_amount", "grand_total", mode="before")
    @classmethod
    def coerce(cls, v): return Decimal(str(v))


class PaginatedOrders(BaseModel):
    total:    int
    page:     int
    per_page: int
    results:  list[OrderOut]


class OrderStatusUpdate(BaseModel):
    status:         str
    tracking_code:  Optional[str] = None
    payment_status: Optional[str] = None


class NewsletterSubscribe(BaseModel):
    email:     EmailStr
    full_name: Optional[str] = None


class NewsletterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:        int
    email:     str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
