from __future__ import annotations
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title:        str
    slug:         str
    tag:          Optional[str]  = None
    subtitle:     Optional[str]  = None
    excerpt:      Optional[str]  = None
    content:      Optional[str]  = None
    cover_image:  Optional[str]  = None
    cover_color:  Optional[str]  = None
    published_at: Optional[date] = None
    is_published: bool = True
    sort_order:   int  = 0


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title:        Optional[str]  = None
    slug:         Optional[str]  = None
    tag:          Optional[str]  = None
    subtitle:     Optional[str]  = None
    excerpt:      Optional[str]  = None
    content:      Optional[str]  = None
    cover_image:  Optional[str]  = None
    cover_color:  Optional[str]  = None
    published_at: Optional[date] = None
    is_published: Optional[bool] = None
    sort_order:   Optional[int]  = None


class PostOut(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id:         int
    created_at: datetime
    updated_at: datetime


class PostListOut(BaseModel):
    """Card ngoài trang danh sách — không kèm HTML thân bài cho nhẹ."""
    model_config = ConfigDict(from_attributes=True)
    id:           int
    title:        str
    slug:         str
    tag:          Optional[str]  = None
    subtitle:     Optional[str]  = None
    excerpt:      Optional[str]  = None
    cover_image:  Optional[str]  = None
    cover_color:  Optional[str]  = None
    published_at: Optional[date] = None
    is_published: bool = True
    sort_order:   int  = 0


class PaginatedPosts(BaseModel):
    total:    int
    page:     int
    per_page: int
    results:  list[PostListOut]
