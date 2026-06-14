from __future__ import annotations
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CustomizationOptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:               int
    group_key:        str
    group_label:      str
    option_key:       str
    option_label:     str
    price_adjustment: Decimal
    sort_order:       int
    is_active:        bool


class CustomizationGroupOut(BaseModel):
    group_key:   str
    group_label: str
    options:     list[CustomizationOptionOut]


class CustomizationOptionCreate(BaseModel):
    group_key:        str
    group_label:      str
    option_key:       str
    option_label:     str
    price_adjustment: Decimal = Decimal("0")
    sort_order:       int     = 0


class CustomizationOptionUpdate(BaseModel):
    group_label:      Optional[str]     = None
    option_label:     Optional[str]     = None
    price_adjustment: Optional[Decimal] = None
    sort_order:       Optional[int]     = None
    is_active:        Optional[bool]    = None
