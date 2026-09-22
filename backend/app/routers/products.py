from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File, status
from peewee import fn, DoesNotExist, IntegrityError

from app.models.product import Product, ProductImage, ProductSize, Category
from app.models.category import SubCategory
from app.schemas.product import (
    ProductOut, ProductListOut, ProductCreate, ProductUpdate,
    PaginatedProducts, CategoryOut, CategoryCreate, CategoryUpdate,
    SubCategoryOut, SubCategoryCreate, SubCategoryUpdate,
    ProductImageUpdate, ProductSizeOut, SizeCreate, SizeUpdate,
)
from app.auth import require
from app.database import get_db

router = APIRouter(prefix="/api/products", tags=["Products"])
cat_router = APIRouter(prefix="/api/categories", tags=["Categories"])
sub_router = APIRouter(prefix="/api/subcategories", tags=["SubCategories"])


# ── helpers ──────────────────────────────────────────────────────────────
FABRIC_CATEGORY_SLUG = "lua-to-tam"


def _is_fabric_category(category_id: Optional[int], subcategory_id: Optional[int]) -> bool:
    """Sản phẩm có nằm trong nhánh danh mục 'Lụa tơ tằm' hay không."""
    if category_id:
        cat = Category.get_or_none(Category.id == category_id)
        if cat and cat.slug == FABRIC_CATEGORY_SLUG:
            return True
    if subcategory_id:
        sub = SubCategory.get_or_none(SubCategory.id == subcategory_id)
        if sub:
            cat = Category.get_or_none(Category.id == sub.category_id)
            if cat and cat.slug == FABRIC_CATEGORY_SLUG:
                return True
    return False


def _resolve_product_type(p: Product) -> str:
    """Sản phẩm cũ (tạo trước khi có field này) → suy ra từ danh mục."""
    ptype = getattr(p, "product_type", None)
    if ptype:
        return ptype
    return "fabric" if _is_fabric_category(p.category_id, p.subcategory_id) else "apparel"


def _product_to_out(p: Product) -> dict:
    images = list(
        ProductImage.select()
        .where(ProductImage.product == p)
        .order_by(ProductImage.sort_order, ProductImage.id)
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
        "compare_at_price": Decimal(str(p.compare_at_price)) if p.compare_at_price is not None else None,
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
        "subcategory_id":   p.subcategory_id,
        "created_at":       p.created_at,
        "updated_at":       p.updated_at,
        "primary_color": p.primary_color,
        "product_type":     _resolve_product_type(p),
        "sku_code":         p.sku_code,
        "specification":    p.specification,
        "fabric_width":     p.fabric_width,
        "unit_label":       p.unit_label,
        "pattern":          p.pattern,
        "color_tag":        p.color_tag,
        "silk_type":        p.silk_type,
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


def _filter_by_category(qs, cat_id: int):
    """Lọc theo danh mục cha — bắt cả sản phẩm chỉ được gán danh mục con của nó."""
    sub_ids = [
        s.id for s in SubCategory.select(SubCategory.id).where(SubCategory.category == cat_id)
    ]
    cond = Product.category == cat_id
    if sub_ids:
        cond = cond | (Product.subcategory << sub_ids)
    return qs.where(cond)


# ══════════════════════════════════════════════════════════════════════════
# CATEGORY endpoints
# ══════════════════════════════════════════════════════════════════════════
@cat_router.get("/", response_model=list[CategoryOut])
def list_categories(active_only: bool = True):
    qs = Category.select().order_by(Category.sort_order, Category.name)
    if active_only:
        qs = qs.where(Category.is_active == True)
    result = []
    for c in qs:
        subs = list(SubCategory.select().where(SubCategory.category == c).order_by(SubCategory.sort_order, SubCategory.name))
        out = CategoryOut.model_validate(c, from_attributes=True)
        out.subcategories = [SubCategoryOut.model_validate(s, from_attributes=True) for s in subs]
        result.append(out)
    return result


@cat_router.get("/{slug}", response_model=CategoryOut)
def get_category(slug: str):
    try:
        cat = Category.get(Category.slug == slug)
        return CategoryOut.model_validate(cat, from_attributes=True)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")


@cat_router.post("/", response_model=CategoryOut, status_code=201,
                 dependencies=[Depends(require("categories.create"))])
def create_category(data: CategoryCreate):
    cat = Category.create(**data.model_dump())
    return CategoryOut.model_validate(cat, from_attributes=True)


@cat_router.put("/{cat_id}", response_model=CategoryOut,
                dependencies=[Depends(require("categories.update"))])
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
    page:            int            = Query(1, ge=1),
    per_page:        int            = Query(12, ge=1, le=100),
    category:        Optional[str]  = Query(None, description="category slug"),
    category_id:     Optional[int]  = Query(None, description="category id"),
    subcategory:     Optional[str]  = Query(None, description="subcategory slug"),
    subcategory_id:  Optional[int]  = Query(None, description="subcategory id"),
    search:          Optional[str]  = Query(None),
    is_new:          Optional[bool] = Query(None),
    is_featured:     Optional[bool] = Query(None),
    _db=Depends(get_db),
):
    qs = (
        Product.select()
        .where(Product.is_active == True)
        .order_by(Product.sort_order, Product.created_at.desc())
    )
    if category:
        cat = Category.get_or_none(Category.slug == category)
        if cat is None:
            # slug không tồn tại → danh sách rỗng, không phải lỗi
            return PaginatedProducts(total=0, page=page, per_page=per_page, results=[])
        qs = _filter_by_category(qs, cat.id)
    if category_id:
        qs = _filter_by_category(qs, category_id)
    if subcategory:
        sub = SubCategory.get_or_none(SubCategory.slug == subcategory)
        if sub is None:
            return PaginatedProducts(total=0, page=page, per_page=per_page, results=[])
        qs = qs.where(Product.subcategory == sub.id)
    if subcategory_id:
        qs = qs.where(Product.subcategory == subcategory_id)
    if search:
        qs = qs.where(
            fn.LOWER(Product.name).contains(search.lower()) |
            fn.LOWER(Product.description).contains(search.lower())
        )
    if is_new is not None:
        qs = qs.where(Product.is_new == is_new)
    if is_featured is not None:
        qs = qs.where(Product.is_featured == is_featured)

    total   = qs.count()
    records = list(qs.offset((page - 1) * per_page).limit(per_page))
    results = [ProductListOut.model_validate(_product_to_out(p)) for p in records]
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
        if slug.isdigit():
            p = Product.get_by_id(int(slug))
        else:
            p = Product.get(Product.slug == slug, Product.is_active == True)
        return ProductOut.model_validate(_product_to_out(p))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/", response_model=ProductOut, status_code=201,
             dependencies=[Depends(require("products.create"))])
def create_product(data: ProductCreate, _db=Depends(get_db)):
    sizes     = data.sizes
    color_hex = data.color_hex or data.primary_color  # accept both fields
    payload   = data.model_dump(exclude={"sizes", "color_hex", "primary_color"})
    if color_hex:
        payload["primary_color"] = color_hex
    payload.pop("sub_category", None)   # field chỉ để đọc, tên sub lấy từ FK

    sub_id = payload.pop("subcategory_id", None)
    if sub_id:
        try:
            sub = SubCategory.get_by_id(sub_id)
        except DoesNotExist:
            raise HTTPException(status_code=400, detail="Danh mục con không tồn tại.")
        if payload.get("category_id") and sub.category_id != payload["category_id"]:
            raise HTTPException(
                status_code=400,
                detail="Danh mục con không thuộc danh mục đã chọn.",
            )
        payload["subcategory"] = sub_id

    # Không chọn loại → suy ra từ danh mục (nhánh "Lụa tơ tằm" = vải)
    if not payload.get("product_type"):
        payload["product_type"] = (
            "fabric"
            if _is_fabric_category(payload.get("category_id"), sub_id)
            else "apparel"
        )

    if Product.select().where(Product.slug == payload["slug"]).exists():
        raise HTTPException(
            status_code=409,
            detail=f"Slug '{payload['slug']}' đã được dùng cho sản phẩm khác. "
                   f"Vui lòng đổi slug (ví dụ thêm hậu tố: {payload['slug']}-2).",
        )

    try:
        product = Product.create(**payload)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=f"Slug '{payload['slug']}' đã tồn tại. Vui lòng chọn slug khác.",
        )

    from app.storage import save_placeholder
    placeholder_url = save_placeholder(product.slug, product.name, color_hex)
    ProductImage.create(
        product=product,
        url=placeholder_url,
        alt_text=product.name,
        sort_order=0,
        is_primary=True,
    )
    for sz in sizes:
        ProductSize.create(product=product, size=sz)

    return ProductOut.model_validate(_product_to_out(product))


def _unique_slug(base: str) -> str:
    """base-copy, base-copy-2, … — slug là unique nên phải dò tới khi còn trống."""
    base = base[:240]            # chừa chỗ cho hậu tố, cột slug tối đa 255 ký tự
    candidate = f"{base}-copy"
    n = 1
    while Product.select().where(Product.slug == candidate).exists():
        n += 1
        candidate = f"{base}-copy-{n}"
    return candidate


@router.post("/{product_id}/duplicate", response_model=ProductOut, status_code=201,
             dependencies=[Depends(require("products.create"))])
def duplicate_product(product_id: int, _db=Depends(get_db)):
    """
    Nhân bản một sản phẩm: copy toàn bộ thông tin, ảnh và size sang sản phẩm mới.

    Bản sao được tạo ở trạng thái ẨN (is_active=False) để không lộ ra cửa hàng
    trước khi admin sửa xong tên / giá / ảnh.

    Ảnh dùng chung URL với bản gốc chứ không nhân đôi file trên storage —
    delete_image chỉ xoá file thật khi không còn sản phẩm nào dùng ảnh đó.
    """
    try:
        src = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")

    suffix = " (bản sao)"
    copy_name = f"{src.name[:255 - len(suffix)]}{suffix}"

    with _db.atomic():
        new = Product.create(
            name=copy_name,
            slug=_unique_slug(src.slug),
            is_active=False,
            price=src.price,
            compare_at_price=src.compare_at_price,
            description=src.description,
            fabric=src.fabric,
            care_instructions=src.care_instructions,
            shipping_info=src.shipping_info,
            category=src.category_id,
            subcategory=src.subcategory_id,
            collection=src.collection_id,
            is_new=src.is_new,
            is_featured=src.is_featured,
            sort_order=src.sort_order,
            primary_color=src.primary_color,
            product_type=src.product_type,
            sku_code=src.sku_code,
            specification=src.specification,
            fabric_width=src.fabric_width,
            unit_label=src.unit_label,
            pattern=src.pattern,
            color_tag=src.color_tag,
            silk_type=src.silk_type,
        )

        images = (
            ProductImage.select()
            .where(ProductImage.product == src)
            .order_by(ProductImage.sort_order, ProductImage.id)
        )
        for img in images:
            ProductImage.create(
                product=new,
                url=img.url,
                alt_text=img.alt_text,
                sort_order=img.sort_order,
                is_primary=img.is_primary,
            )

        sizes = ProductSize.select().where(ProductSize.product == src).order_by(ProductSize.id)
        for sz in sizes:
            ProductSize.create(
                product=new,
                size=sz.size,
                stock=sz.stock,
                is_available=sz.is_available,
                sort_order=sz.sort_order,
            )

    return ProductOut.model_validate(_product_to_out(new))


@router.put("/{product_id}", response_model=ProductOut,
            dependencies=[Depends(require("products.update"))])
def update_product(product_id: int, data: ProductUpdate, _db=Depends(get_db)):
    try:
        p = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    changes = data.model_dump(exclude_none=True)
    changes.pop("sub_category", None)   # field chỉ để đọc

    sub_id = changes.pop("subcategory_id", None)
    if sub_id is not None:
        try:
            sub = SubCategory.get_by_id(sub_id)
        except DoesNotExist:
            raise HTTPException(status_code=400, detail="Danh mục con không tồn tại.")
        target_cat = changes.get("category_id", p.category_id)
        if target_cat and sub.category_id != target_cat:
            raise HTTPException(
                status_code=400,
                detail="Danh mục con không thuộc danh mục đã chọn.",
            )
        changes["subcategory"] = sub_id

    new_slug = changes.get("slug")
    if new_slug and new_slug != p.slug and (
        Product.select().where(Product.slug == new_slug, Product.id != p.id).exists()
    ):
        raise HTTPException(
            status_code=409,
            detail=f"Slug '{new_slug}' đã được dùng cho sản phẩm khác. Vui lòng chọn slug khác.",
        )

    for field, val in changes.items():
        setattr(p, field, val)
    try:
        p.save()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Slug đã tồn tại. Vui lòng chọn slug khác.")
    return ProductOut.model_validate(_product_to_out(p))


@router.delete("/{product_id}", status_code=204,
               dependencies=[Depends(require("products.delete"))])
def delete_product(product_id: int, _db=Depends(get_db)):
    try:
        p = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    p.is_active = False   # soft delete
    p.save()


@router.post("/{product_id}/images", status_code=201,
             dependencies=[Depends(require("products.update"))])
def upload_image(
    product_id: int,
    file:       UploadFile = File(...),
    color_hex:  Optional[str] = None,
    _db=Depends(get_db),
):
    from app.storage import upload_file
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")

    file_bytes   = file.file.read()
    content_type = file.content_type or "image/jpeg"
    public_url   = upload_file(file_bytes, file.filename or "image.jpg", product_id, content_type)

    next_pos = (
        ProductImage.select(fn.COALESCE(fn.MAX(ProductImage.sort_order), -1))
        .where(ProductImage.product == product)
        .scalar()
        + 1
    )
    img = ProductImage.create(
        product=product,
        url=public_url,
        alt_text=product.name,
        sort_order=next_pos,
        is_primary=False,
    )
    if color_hex and not product.primary_color:
        product.primary_color = color_hex
        product.save(only=[Product.primary_color])
    return {"id": img.id, "url": img.url, "position": img.sort_order}


@router.put("/{product_id}/images/{img_id}",
            dependencies=[Depends(require("products.update"))])
def update_image(product_id: int, img_id: int, data: ProductImageUpdate, _db=Depends(get_db)):
    try:
        img = ProductImage.get(ProductImage.id == img_id, ProductImage.product == product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Image not found")
    if data.is_primary:
        ProductImage.update(is_primary=False).where(ProductImage.product == product_id).execute()
        img.is_primary = True
    if data.alt_text is not None:
        img.alt_text = data.alt_text
    if data.sort_order is not None:
        img.sort_order = data.sort_order
    img.save()
    return {"id": img.id, "url": img.url, "position": img.sort_order, "is_primary": img.is_primary}


@router.patch("/{product_id}/images/reorder",
              dependencies=[Depends(require("products.update"))])
def reorder_images(product_id: int, data: list[dict], _db=Depends(get_db)):
    """data = [{ id: int, sort_order: int }, ...]"""
    try:
        Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    for item in data:
        ProductImage.update(sort_order=item["sort_order"]).where(
            ProductImage.id == item["id"],
            ProductImage.product == product_id,
        ).execute()
    return {"ok": True}


@router.delete("/{product_id}/images/{img_id}", status_code=204,
               dependencies=[Depends(require("products.update"))])
def delete_image(product_id: int, img_id: int, _db=Depends(get_db)):
    from app.storage import delete_file
    try:
        img = ProductImage.get(ProductImage.id == img_id, ProductImage.product == product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Image not found")

    # Sản phẩm nhân bản dùng chung URL ảnh với bản gốc — xoá file ngay sẽ làm
    # hỏng ảnh của sản phẩm kia, nên chỉ xoá khi không còn bản ghi nào trỏ tới.
    still_used = (
        ProductImage.select()
        .where(ProductImage.url == img.url, ProductImage.id != img.id)
        .exists()
    )
    if not still_used:
        delete_file(img.url)
    img.delete_instance()


# ── Size endpoints ────────────────────────────────────────────────────────
@router.post("/{product_id}/sizes", response_model=ProductSizeOut, status_code=201,
             dependencies=[Depends(require("products.update"))])
def add_size(product_id: int, data: SizeCreate, _db=Depends(get_db)):
    try:
        product = Product.get_by_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    s = ProductSize.create(product=product, size=data.size, is_available=data.is_available)
    return ProductSizeOut(id=s.id, size=s.size, in_stock=s.is_available)


@router.put("/{product_id}/sizes/{size_id}", response_model=ProductSizeOut,
            dependencies=[Depends(require("products.update"))])
def update_size(product_id: int, size_id: int, data: SizeUpdate, _db=Depends(get_db)):
    try:
        s = ProductSize.get(ProductSize.id == size_id, ProductSize.product == product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Size not found")
    if data.size is not None:
        s.size = data.size
    if data.is_available is not None:
        s.is_available = data.is_available
    s.save()
    return ProductSizeOut(id=s.id, size=s.size, in_stock=s.is_available)


@router.delete("/{product_id}/sizes/{size_id}", status_code=204,
               dependencies=[Depends(require("products.update"))])
def delete_size(product_id: int, size_id: int, _db=Depends(get_db)):
    try:
        s = ProductSize.get(ProductSize.id == size_id, ProductSize.product == product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Size not found")
    s.delete_instance()


# ── Category DELETE ────────────────────────────────────────────────────────
@cat_router.delete("/{cat_id}", status_code=204,
                   dependencies=[Depends(require("categories.delete"))])
def delete_category(cat_id: int, _db=Depends(get_db)):
    try:
        cat = Category.get_by_id(cat_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.delete_instance()


# ── SubCategory endpoints ──────────────────────────────────────────────────
@cat_router.get("/{cat_id}/subcategories", response_model=list[SubCategoryOut])
def list_subcategories(cat_id: int, _db=Depends(get_db)):
    try:
        cat = Category.get_by_id(cat_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
    subs = SubCategory.select().where(SubCategory.category == cat).order_by(SubCategory.sort_order, SubCategory.name)
    return [SubCategoryOut.model_validate(s, from_attributes=True) for s in subs]


@cat_router.post("/{cat_id}/subcategories", response_model=SubCategoryOut, status_code=201,
                 dependencies=[Depends(require("categories.create"))])
def create_subcategory(cat_id: int, data: SubCategoryCreate, _db=Depends(get_db)):
    try:
        cat = Category.get_by_id(cat_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
    sub = SubCategory.create(category=cat, **data.model_dump())
    return SubCategoryOut.model_validate(sub, from_attributes=True)


@sub_router.put("/{sub_id}", response_model=SubCategoryOut,
                dependencies=[Depends(require("categories.update"))])
def update_subcategory(sub_id: int, data: SubCategoryUpdate, _db=Depends(get_db)):
    try:
        sub = SubCategory.get_by_id(sub_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(sub, field, val)
    sub.save()
    return SubCategoryOut.model_validate(sub, from_attributes=True)


@sub_router.delete("/{sub_id}", status_code=204,
                   dependencies=[Depends(require("categories.delete"))])
def delete_subcategory(sub_id: int, _db=Depends(get_db)):
    try:
        sub = SubCategory.get_by_id(sub_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    sub.delete_instance()
