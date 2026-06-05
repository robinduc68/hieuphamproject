from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class OrderItemIn(BaseModel):
    product_id: int
    size:       str
    quantity:   int = 1

class OrderCreate(BaseModel):
    email:     EmailStr
    full_name: str
    phone:     str
    address:   str
    city:      str
    country:   str = "Vietnam"
    note:      Optional[str] = None
    items:     list[OrderItemIn]

class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:         int
    product_id: int
    size:       str
    quantity:   int
    price:      Decimal

    @field_validator("price", mode="before")
    @classmethod
    def coerce(cls, v): return Decimal(str(v))

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:            int
    email:         str
    full_name:     str
    phone:         str
    address:       str
    city:          str
    country:       str
    note:          Optional[str] = None
    total:         Decimal
    status:        str
    tracking_code: Optional[str] = None
    items:         list[OrderItemOut] = []
    created_at:    datetime

    @field_validator("total", mode="before")
    @classmethod
    def coerce(cls, v): return Decimal(str(v))

class OrderStatusUpdate(BaseModel):
    status:        str
    tracking_code: Optional[str] = None

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
