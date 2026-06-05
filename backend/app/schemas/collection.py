from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CollectionBase(BaseModel):
    title:        str
    subtitle:     Optional[str] = None
    slug:         str
    description:  Optional[str] = None
    gradient:     Optional[str] = None
    accent_color: Optional[str] = None
    cover_image:  Optional[str] = None
    is_tall:      bool = False
    is_active:    bool = True
    sort_order:   int  = 0

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    title:        Optional[str]  = None
    subtitle:     Optional[str]  = None
    description:  Optional[str]  = None
    gradient:     Optional[str]  = None
    accent_color: Optional[str]  = None
    cover_image:  Optional[str]  = None
    is_tall:      Optional[bool] = None
    is_active:    Optional[bool] = None
    sort_order:   Optional[int]  = None

class CollectionOut(CollectionBase):
    model_config = ConfigDict(from_attributes=True)
    id:         int
    created_at: datetime
    updated_at: datetime
