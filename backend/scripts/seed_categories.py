#!/usr/bin/env python
"""
Seed danh mục sản phẩm theo đúng cây danh mục đang hiển thị trên website:

    Áo dài      → Áo dài 2 tà / Áo dài 4 tà / Áo dài thêu tay
    Pháp phục
    Đầm lụa
    Khăn lụa    → Khăn lụa vẽ tay / loang tia / trơn cao cấp
    Lụa tơ tằm  → Lụa Nha Xá thông dụng / Lụa Nha Xá 100% tơ tằm

Script chạy được nhiều lần (idempotent): khớp theo slug, có thì cập nhật tên,
chưa có thì tạo mới. Không đụng tới các danh mục khác mà admin tự thêm.

Cách chạy (trong container backend):
    docker exec -it huyvo_backend python scripts/seed_categories.py

Tuỳ chọn:
    --remap      chuyển sản phẩm đang nằm ở danh mục cũ sang danh mục mới
                 (Modern Heritage → Áo dài, sản phẩm tên "lụa tơ tằm" → Lụa tơ tằm)
    --drop-old   xoá 3 danh mục cũ modern-heritage / womenswear / menswear
                 (sản phẩm không bị xoá — FK là SET NULL, nên nhớ chạy kèm --remap)
    --yes        bỏ qua bước gõ xác nhận
"""
import argparse
import sys

sys.path.insert(0, "/app")

from app.database import db
from app.models.category import Category, SubCategory
from app.models.product import Product
from app.taxonomy import TAXONOMY, LEGACY_SLUGS

# Danh mục cũ → danh mục mới khi chạy --remap
LEGACY_TO_NEW = {
    "modern-heritage": "ao-dai",
    "womenswear":      "ao-dai",
    "menswear":        "ao-dai",
}

# Tên sản phẩm chứa chuỗi này thì ưu tiên đẩy về danh mục tương ứng
NAME_HINTS = [
    ("lụa tơ tằm", "lua-to-tam"),
    ("lua to tam", "lua-to-tam"),
    ("khăn lụa",   "khan-lua"),
    ("đầm lụa",    "dam-lua"),
    ("pháp phục",  "phap-phuc"),
]


def seed():
    """Tạo / cập nhật cây danh mục. Trả về dict slug → Category."""
    cats = {}
    for order, (slug, name, subs) in enumerate(TAXONOMY):
        cat = Category.get_or_none(Category.slug == slug)
        if cat is None:
            cat = Category.create(name=name, slug=slug, sort_order=order, is_active=True)
            print(f"  + tạo danh mục   {slug:<12} {name}")
        else:
            cat.name, cat.sort_order, cat.is_active = name, order, True
            cat.save()
            print(f"  = giữ danh mục   {slug:<12} {name}")
        cats[slug] = cat

        for sub_order, (sub_slug, sub_name) in enumerate(subs):
            sub = SubCategory.get_or_none(SubCategory.slug == sub_slug)
            if sub is None:
                SubCategory.create(
                    category=cat, name=sub_name, slug=sub_slug,
                    sort_order=sub_order, is_active=True,
                )
                print(f"      + tạo con    {sub_slug:<28} {sub_name}")
            else:
                sub.category, sub.name = cat, sub_name
                sub.sort_order, sub.is_active = sub_order, True
                sub.save()
                print(f"      = giữ con    {sub_slug:<28} {sub_name}")
    return cats


def pick_target(product, cats, legacy_slug):
    """Chọn danh mục mới cho 1 sản phẩm: ưu tiên gợi ý từ tên, sau đó map cứng."""
    name = (product.name or "").lower()
    for needle, slug in NAME_HINTS:
        if needle in name:
            return cats[slug]
    target_slug = LEGACY_TO_NEW.get(legacy_slug)
    return cats.get(target_slug) if target_slug else None


def remap(cats):
    """Chuyển sản phẩm ở danh mục cũ (và sản phẩm chưa có danh mục) sang cây mới."""
    legacy = {c.slug: c for c in Category.select().where(Category.slug.in_(LEGACY_SLUGS))}
    legacy_ids = {c.id: slug for slug, c in legacy.items()}
    new_ids = {c.id for c in cats.values()}

    moved = skipped = 0
    for p in Product.select():
        if p.category_id in new_ids:
            continue  # đã nằm trong cây mới
        legacy_slug = legacy_ids.get(p.category_id)
        if p.category_id is not None and legacy_slug is None:
            continue  # danh mục do admin tự thêm — không đụng vào
        target = pick_target(p, cats, legacy_slug)
        if target is None:
            skipped += 1
            continue
        old = legacy_slug or "(chưa có)"
        p.category = target
        p.subcategory = None  # danh mục con cũ không còn thuộc danh mục mới
        p.save()
        moved += 1
        print(f"  → #{p.id:<4} {old:<16} ⇒ {target.slug:<12} {p.name.strip()}")

    print(f"\n  Đã chuyển {moved} sản phẩm" + (f", bỏ qua {skipped}" if skipped else ""))
    print("  Danh mục con của sản phẩm đã xoá — vào admin chọn lại cho đúng.")


def drop_old():
    rows = list(Category.select().where(Category.slug.in_(LEGACY_SLUGS)))
    if not rows:
        print("  Không còn danh mục cũ nào.")
        return
    for c in rows:
        n = Product.select().where(Product.category == c).count()
        c.delete_instance()  # subcategories CASCADE, products SET NULL
        print(f"  - xoá {c.slug} (còn {n} sản phẩm → chuyển thành chưa phân loại)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--remap", action="store_true")
    ap.add_argument("--drop-old", action="store_true")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    if (args.remap or args.drop_old) and not args.yes:
        print("Sẽ thay đổi dữ liệu sản phẩm/danh mục hiện có.")
        if input('Gõ "yes" để tiếp tục: ').strip().lower() != "yes":
            print("Đã huỷ.")
            return

    db.connect(reuse_if_open=True)
    try:
        with db.atomic():
            print("\n── Danh mục ──")
            cats = seed()
            if args.remap:
                print("\n── Chuyển sản phẩm ──")
                remap(cats)
            if args.drop_old:
                print("\n── Xoá danh mục cũ ──")
                drop_old()
        print("\nXong.\n")
    finally:
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    main()
