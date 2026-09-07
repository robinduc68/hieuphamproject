"""
Bài viết trang "Tin tức" — danh sách, trang chi tiết và CRUD cho trang admin.
Nội dung thân bài là HTML soạn trong admin (giống mô tả sản phẩm).
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from peewee import DoesNotExist, IntegrityError

from app.auth import require
from app.database import get_db
from app.models.post import Post
from app.schemas.post import (
    PaginatedPosts, PostCreate, PostListOut, PostOut, PostUpdate,
)

router = APIRouter(prefix="/api/posts", tags=["Posts"])


def _ordered():
    return Post.select().order_by(
        Post.sort_order, Post.published_at.desc(nulls="LAST"), Post.id.desc()
    )


@router.get("/", response_model=PaginatedPosts)
def list_posts(
    page:        int  = Query(1, ge=1),
    per_page:    int  = Query(12, ge=1, le=100),
    search:      Optional[str]  = Query(None),
    # Web khách chỉ thấy bài đã đăng; trang admin gọi với published_only=false
    published_only: bool = Query(True),
    _db=Depends(get_db),
):
    qs = _ordered()
    if published_only:
        qs = qs.where(Post.is_published == True)
    if search:
        qs = qs.where(Post.title.contains(search))

    total   = qs.count()
    records = list(qs.offset((page - 1) * per_page).limit(per_page))
    return PaginatedPosts(
        total=total, page=page, per_page=per_page,
        results=[PostListOut.model_validate(p, from_attributes=True) for p in records],
    )


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, _db=Depends(get_db)):
    """Nhận slug hoặc id — trang admin sửa bài gọi bằng id."""
    post = Post.get_or_none(Post.slug == slug)
    if post is None and slug.isdigit():
        post = Post.get_or_none(Post.id == int(slug))
    if post is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết.")
    return PostOut.model_validate(post, from_attributes=True)


@router.get("/{slug}/related", response_model=list[PostListOut])
def related_posts(slug: str, limit: int = Query(2, ge=1, le=12), _db=Depends(get_db)):
    qs = _ordered().where(Post.is_published == True, Post.slug != slug).limit(limit)
    return [PostListOut.model_validate(p, from_attributes=True) for p in qs]


@router.post("/", response_model=PostOut, status_code=201,
             dependencies=[Depends(require("posts.create"))])
def create_post(data: PostCreate, _db=Depends(get_db)):
    payload = data.model_dump()
    if Post.select().where(Post.slug == payload["slug"]).exists():
        raise HTTPException(
            status_code=409,
            detail=f"Slug '{payload['slug']}' đã được dùng cho bài viết khác.",
        )
    try:
        post = Post.create(**payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Slug đã tồn tại. Vui lòng chọn slug khác.")
    return PostOut.model_validate(post, from_attributes=True)


@router.put("/{post_id}", response_model=PostOut,
            dependencies=[Depends(require("posts.update"))])
def update_post(post_id: int, data: PostUpdate, _db=Depends(get_db)):
    try:
        post = Post.get_by_id(post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết.")

    changes = data.model_dump(exclude_unset=True)
    new_slug = changes.get("slug")
    if new_slug and new_slug != post.slug and (
        Post.select().where(Post.slug == new_slug, Post.id != post.id).exists()
    ):
        raise HTTPException(
            status_code=409,
            detail=f"Slug '{new_slug}' đã được dùng cho bài viết khác.",
        )

    for field, val in changes.items():
        setattr(post, field, val)
    try:
        post.save()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Slug đã tồn tại. Vui lòng chọn slug khác.")
    return PostOut.model_validate(post, from_attributes=True)


@router.delete("/{post_id}", status_code=204,
               dependencies=[Depends(require("posts.delete"))])
def delete_post(post_id: int, _db=Depends(get_db)):
    try:
        post = Post.get_by_id(post_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết.")
    post.delete_instance()
