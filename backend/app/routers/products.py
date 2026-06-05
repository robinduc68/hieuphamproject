from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File, status
from peewee import fn, DoesNotExist, SQL

from app.models.product import Product, ProductImage, ProductSize, Category
from app.schemas.product import (
    ProductOut, ProductListOut, ProductCreate, ProductUpdate,
    PaginatedProducts, CategoryOut, CategoryCreate, CategoryUpdate,
)
from app.auth import get_current_admin
from app.database import get_db

router = APIRouter(prefix="/api/products", tags=["Products"])
cat_router = APIRouter(prefix="/api/categories", tags=["Categories"])


# ── helpers ──────────────────────────────────────────────────────────────
def _product_to_out(p: Product) -> dict:
    images = list(
        ProductImage.select()
        .where(ProductImage.product == p)
        .order_by(SQL("product_images.sort_order"), SQL("product_images.id"))
    )
    sizes = list(
        ProductSize.select()
        .where(ProductSize.product == p)
        .order_by(ProductSize.id)
    )
    data = {
        "id":               p.id,
        "name":             p.name,
        "slug":             p.slug,
        "price":            Decimal(str(p.price)),
        "description":      p.description,
        "fabric":           p.fabric,
        "care_instructions": p.care_instructions,
        "shipping_info":    p.shipping_info,
        "sub_category":     p.subcategory.name if getattr(p, "subcategory_id", None) else None,
        "is_new":           p.is_new,
        "is_active":        p.is_active,
        "is_featured":      p.is_featured,
        "sort_order":       p.sort_order,
        "category_id":      p.category_id,
        "created_at":       p.created_at,
        "updated_at":       p.updated_at,
        "images": [
            {
                "id": i.id,
                "url": i.url,
                "color_hex": p.primary_color,
                "alt_text": i.alt_text,
                "position": i.sort_order,
            }
            for i in images
        ],
        "sizes": [
            {"id": s.id, "size": s.size, "in_stock": s.is_available}
            for s in sizes
        ],
    }
    if p.category_id:
        try:
            cat = Category.get_by_id(p.category_id)
            data["category"] = {
                "id": cat.id, "name": cat.name, "slug": cat.slug,
                "description": cat.description, "sort_order": cat.sort_order,
                "is_active": cat.is_active, "parent_id": None,
                "created_at": cat.created_at, "updated_at": cat.updated_at,
            }
        except DoesNotExist:
            data["category"] = None
    else:
        data["category"] = None
    return data


# ══════════════════════════════════════════════════════════════════════════
# CATEGORY endpoints
# ══════════════════════════════════════════════════════════════════════════
@cat_router.get("/", response_model=list[CategoryOut])
def list_categories(active_only: bool = True):
    qs = Category.select().order_by(Category.sort_order, Category.name)
    if active_only:
        qs = qs.where(Category.is_active == True)
    return [CategoryOut.model_validate(c, from_attributes=True) for c in qs]


@cat_router.get("/{slug}", response_model=CategoryOut)
def get_category(slug: str):
    try:
        cat = Category.get(Category.slug == slug)
        return CategoryOut.model_validate(cat, from_attributes=True)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")


@cat_router.post("/", response_model=CategoryOut, status_code=201,
                 dependencies=[Depends(get_current_admin)])
def create_category(data: CategoryCreate):
    cat = Category.create(**data.model_dump())
    return CategoryOut.model_validate(cat, from_attributes=True)


@cat_router.put("/{cat_id}", response_model=CategoryOut,
                dependencies=[Depends(get_current_admin)])
def update_category(cat_id: int, data: CategoryUpdate):
    try:
        cat = Category.get_by_id(cat_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(cat, field, val)
    cat.save()
    return CategoryOut.model_validate(cat, from_attributes=True)


# ══════════════════════════════════════════════════════════════════════════
# PRODUCT endpoints
# ══════════════════════════════════════════════════════════════════════════
@router.get("/", response_model=PaginatedProducts)
def list_products(
    page:        int            = Query(1, ge=1),
    per_page:    int            = Query(12, ge=1, le=100),
    category:    Optional[str]  = Query(None, description="category slug"),
    search:      Optional[str]  = Query(None),
    is_new:      Optional[bool] = Query(None),
    is_featured: Optional[bool] = Query(None),
    _db=Depends(get_db),
):
    print(33333333)
    qs = (
        Product.select()
        .where(Product.is_active == True)
        .order_by(Product.created_at.desc())
    )
    print(1212121221, qs)
    if category:
        try:
            cat = Category.get(Category.slug == category)
            qs = qs.where(Product.category == cat)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")
    print(82828282, qs)
    if search:
        qs = qs.where(
            fn.LOWER(Product.name).contains(search.lower()) |
            fn.LOWER(Product.description).contains(search.lower())
        )
    print(8383883, qs)
    if is_new is not None:
        qs = qs.where(Product.is_new == is_new)
    print(8484884, qs)
    if is_featured is not None:
        qs = qs.where(Product.is_featured == is_featured)
    print(6466464, qs)

    total   = qs.count()
    records = list(qs.offset((page - 1) * per_page).limit(per_page))
    print(737373)
    results = []
    print(5555 ,records)
    for p in records:
        d = _product_to_out(p)
        results.append(ProductListOut.model_validate(d))
    return PaginatedProducts(total=total, page=page, per_page=per_page, results=results)


@router.get("/new-arrivals", response_model=list[ProductListOut])
def new_arrivals(limit: int = Query(10, le=50), _db=Depends(get_db)):
    qs = (
        Product.select()
        .where(Product.is_active == True, Product.is_new == True)
        .order_by(Product.created_at.desc())
        .limit(limit)
    )
    return [ProductListOut.model_validate(_product_to_out(p)) for p in qs]


@router.get("/featured", response_model=list[ProductListOut])
def featured_products(limit: int = Query(4, le=20), _db=Depends(get_db)):
    qs = (
        Product.select()
        .where(Product.is_active == True, Product.is_featured == True)
        .order_by(Product.sort_order)
        .limit(limit)
    )
    return [ProductListOut.model_validate(_product_to_out(p)) for p in qs]


@router.get("/{slug}", response_model=ProductOut)
def get_product(slug: str, _db=Depends(get_db)):
    try:
        p = Product.get(Product.slug == slug, Product.is_active == True)
        return ProductOut.model_validate(_product_to_out(p))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/", response_model=ProductOut, status_code=201,
             dependencies=[Depends(get_current_admin)])
def create_product(data: ProductCreate, _db=Depends(get_db)):
    sizes     = data.sizes
    color_hex = data.color_hex
    payload   = data.model_dump(exclude={"sizes", "color_hex"})
    if color_hex:
        payload["primary_color"] = color_hex
    payload.pop("sub_category", None)
    product = Product.create(**payload)

    ProductImage.create(
        product=product,
        url=f"/media/placeholder/{product.slug}.svg",
        alt_text=product.name,
        sort_order=0,
        is_primary=True,
    )
    for sz in sizes:
        ProductSize.create(product=product, size=sz)

    return ProductOut.model_validate(_product_to_out(product))


@router.put("/{product_id}", response_model=ProductOut,
            dependencies=[Depends(get_current_admin)])
def update_product(product_id: int, data: ProductUpdate, _db=Depends(get_db)):
    try:
        p = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(p, field, val)
    p.save()
    return ProductOut.model_validate(_product_to_out(p))


@router.delete("/{product_id}", status_code=204,
               dependencies=[Depends(get_current_admin)])
def delete_product(product_id: int, _db=Depends(get_db)):
    try:
        p = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    p.is_active = False   # soft delete
    p.save()


@router.post("/{product_id}/images", status_code=201,
             dependencies=[Depends(get_current_admin)])
def upload_image(
    product_id: int,
    file:       UploadFile = File(...),
    color_hex:  Optional[str] = None,
    _db=Depends(get_db),
):
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")

    import os, aiofiles, asyncio
    from app.config import get_settings
    settings = get_settings()
    save_dir = os.path.join(settings.media_dir, "products", str(product_id))
    os.makedirs(save_dir, exist_ok=True)
    fname = f"{product_id}_{file.filename}"
    fpath = os.path.join(save_dir, fname)

    # sync write (keeps router simple; swap to async endpoint if needed)
    with open(fpath, "wb") as f:
        f.write(file.file.read())

    next_pos = (
        ProductImage.select(
            fn.COALESCE(fn.MAX(SQL("product_images.sort_order")), -1),
        )
        .where(ProductImage.product == product)
        .scalar()
        + 1
    )
    img = ProductImage.create(
        product=product,
        url=f"/media/products/{product_id}/{fname}",
        alt_text=product.name,
        sort_order=next_pos,
        is_primary=False,
    )
    if color_hex and not product.primary_color:
        product.primary_color = color_hex
        product.save(only=[Product.primary_color])
    return {"id": img.id, "url": img.url, "position": img.sort_order}
