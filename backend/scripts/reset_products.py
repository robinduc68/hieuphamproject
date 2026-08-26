#!/usr/bin/env python
"""
Xoá sạch sản phẩm để chuẩn bị chạy production.

Xoá:  products + product_images + product_sizes (+ file ảnh trong media)
Giữ:  categories, subcategories, collections, customization_options, user admin

Cách chạy (trong container backend):
    docker exec -it huyvo_backend python scripts/reset_products.py

Tuỳ chọn:
    --with-orders   xoá luôn orders + order_items (đơn hàng test)
    --keep-media    giữ lại file ảnh trong media, chỉ xoá dữ liệu DB
    --yes           bỏ qua bước gõ xác nhận (dùng khi chạy tự động)
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/app")

from app.database import db
from app.models.product import Product, ProductImage, ProductSize
from app.models.order import Order, OrderItem

MEDIA_DIRS = [Path("/app/media/products"), Path("/app/media/placeholder")]


def counts():
    return {
        "products":       Product.select().count(),
        "product_images": ProductImage.select().count(),
        "product_sizes":  ProductSize.select().count(),
        "orders":         Order.select().count(),
        "order_items":    OrderItem.select().count(),
    }


def media_files():
    return [f for d in MEDIA_DIRS if d.exists() for f in d.rglob("*") if f.is_file()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-orders", action="store_true", help="xoá luôn đơn hàng test")
    ap.add_argument("--keep-media",  action="store_true", help="giữ lại file ảnh")
    ap.add_argument("--yes",         action="store_true", help="không hỏi xác nhận")
    args = ap.parse_args()

    if db.is_closed():
        db.connect()

    before = counts()
    files  = [] if args.keep_media else media_files()

    print("\n=== SẼ XOÁ ===")
    print(f"  products        : {before['products']}")
    print(f"  product_images  : {before['product_images']}")
    print(f"  product_sizes   : {before['product_sizes']}")
    if args.with_orders:
        print(f"  orders          : {before['orders']}")
        print(f"  order_items     : {before['order_items']}")
    if not args.keep_media:
        print(f"  file ảnh (media): {len(files)}")

    print("\n=== SẼ GIỮ ===")
    print("  categories, subcategories, collections, customization_options, users (admin)")
    if not args.with_orders and before["orders"]:
        print(f"  orders: {before['orders']} (product_id của order_items sẽ thành NULL "
              f"— dùng --with-orders để xoá luôn)")

    if before["products"] == 0 and not (args.with_orders and before["orders"]):
        print("\nKhông có gì để xoá. Thoát.")
        return

    if not args.yes:
        print("\nThao tác này KHÔNG THỂ hoàn tác.")
        if input('Gõ "XOA" để xác nhận: ').strip() != "XOA":
            print("Đã huỷ, không xoá gì cả.")
            return

    with db.atomic():
        if args.with_orders:
            n_items  = OrderItem.delete().execute()
            n_orders = Order.delete().execute()
            print(f"\n  đã xoá {n_items} order_items, {n_orders} orders")

        # product_images / product_sizes có FK ON DELETE CASCADE,
        # xoá tường minh để đếm được số dòng.
        n_img   = ProductImage.delete().execute()
        n_size  = ProductSize.delete().execute()
        n_prod  = Product.delete().execute()
        print(f"  đã xoá {n_img} ảnh, {n_size} size, {n_prod} sản phẩm")

        # cho sản phẩm mới bắt đầu lại từ id 1
        db.execute_sql("ALTER SEQUENCE products_id_seq RESTART WITH 1;")
        db.execute_sql("ALTER SEQUENCE product_images_id_seq RESTART WITH 1;")
        db.execute_sql("ALTER SEQUENCE product_sizes_id_seq RESTART WITH 1;")
        if args.with_orders:
            db.execute_sql("ALTER SEQUENCE orders_id_seq RESTART WITH 1;")
            db.execute_sql("ALTER SEQUENCE order_items_id_seq RESTART WITH 1;")
        print("  đã reset id sequence về 1")

    if not args.keep_media:
        for d in MEDIA_DIRS:
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True, exist_ok=True)
        print(f"  đã xoá {len(files)} file ảnh trong media")

    after = counts()
    print("\n=== CÒN LẠI ===")
    for k, v in after.items():
        print(f"  {k:15}: {v}")
    print("\nXong. Giờ vào admin nhập sản phẩm thật.\n")


if __name__ == "__main__":
    main()
