from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


# ── SubCategory ────────────────────────────────────────────────────────────
class SubCategoryBase(BaseModel):
    name:        str
    slug:        str
    description: Optional[str] = None
    sort_order:  int = 0
    is_active:   bool = True

class SubCategoryCreate(SubCategoryBase):
    pass

class SubCategoryUpdate(BaseModel):
    name:        Optional[str]  = None
    slug:        Optional[str]  = None
    description: Optional[str]  = None
    sort_order:  Optional[int]  = None
    is_active:   Optional[bool] = None

class SubCategoryOut(SubCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id:          int
    category_id: int
    created_at:  datetime
    updated_at:  datetime


# ── Category ──────────────────────────────────────────────────────────────
class CategoryBase(BaseModel):
    name:        str
    slug:        str
    description: Optional[str] = None
    sort_order:  int = 0
    is_active:   bool = True

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name:        Optional[str]  = None
    description: Optional[str]  = None
    sort_order:  Optional[int]  = None
    is_active:   Optional[bool] = None

class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id:            int
    parent_id:     Optional[int]       = None
    subcategories: list[SubCategoryOut] = []
    created_at:    datetime
    updated_at:    datetime


# ── ProductImage ───────────────────────────────────────────────────────────
class ProductImageUpdate(BaseModel):
    is_primary: Optional[bool] = None
    alt_text:   Optional[str]  = None
    sort_order: Optional[int]  = None

class ProductImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:        int
    url:       str
    color_hex: Optional[str] = None
    alt_text:  Optional[str] = None
    position:  int


# ── ProductSize ────────────────────────────────────────────────────────────
class ProductSizeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:       int
    size:     str
    in_stock: bool

class SizeCreate(BaseModel):
    size:         str
    is_available: bool = True

class SizeUpdate(BaseModel):
    size:         Optional[str]  = None
    is_available: Optional[bool] = None


# ── Product ────────────────────────────────────────────────────────────────
class ProductBase(BaseModel):
    name:              str
    slug:              str
    price:             Decimal
    compare_at_price:  Optional[Decimal] = None
    description:       Optional[str] = None
    fabric:            Optional[str] = None
    care_instructions: Optional[str] = None
    shipping_info:     Optional[str] = None
    sub_category:      Optional[str] = None
    is_new:            bool = False
    is_active:         bool = True
    is_featured:       bool = False
    sort_order:        int  = 0

class ProductCreate(ProductBase):
    category_id:     Optional[int] = None
    subcategory_id:  Optional[int] = None
    sizes:           list[str]     = []
    color_hex:       Optional[str] = None
    primary_color:   Optional[str] = None   # alias cho color_hex, frontend gửi field này

class ProductUpdate(BaseModel):
    name:              Optional[str]     = None
    slug:              Optional[str]     = None
    price:             Optional[Decimal] = None
    compare_at_price:  Optional[Decimal] = None
    description:       Optional[str]     = None
    fabric:            Optional[str]     = None
    care_instructions: Optional[str]     = None
    shipping_info:     Optional[str]     = None
    sub_category:      Optional[str]     = None
    category_id:       Optional[int]     = None
    subcategory_id:    Optional[int]     = None
    primary_color:     Optional[str]     = None
    is_new:            Optional[bool]    = None
    is_active:         Optional[bool]    = None
    is_featured:       Optional[bool]    = None
    sort_order:        Optional[int]     = None

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id:            int
    category_id:   Optional[int]         = None
    subcategory_id: Optional[int]        = None
    category:      Optional[CategoryOut] = None
    primary_color: Optional[str]         = None
    images:        list[ProductImageOut] = []
    sizes:         list[ProductSizeOut]  = []
    created_at:    datetime
    updated_at:    datetime

    @field_validator("price", mode="before")
    @classmethod
    def coerce_decimal(cls, v):
        return Decimal(str(v))

class ProductListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           int
    name:         str
    slug:         str
    price:        Decimal
    compare_at_price: Optional[Decimal] = None
    is_new:       bool
    is_featured:  bool
    sub_category: Optional[str] = None
    category_id:  Optional[int] = None
    category:     Optional[CategoryOut] = None
    images:       list[ProductImageOut] = []
    sizes:        list[ProductSizeOut]  = []

    @field_validator("price", mode="before")
    @classmethod
    def coerce_decimal(cls, v):
        return Decimal(str(v))


# ── Paginated responses ────────────────────────────────────────────────────
class PaginatedProducts(BaseModel):
    total:    int
    page:     int
    per_page: int
    results:  list[ProductListOut]
