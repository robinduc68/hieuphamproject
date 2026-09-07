"""
Migration 0008 – Thuộc tính lọc cho sản phẩm vải

Hai trang kho lụa ngoài website có bộ lọc ở sidebar, trước đây chỉ chạy được
với dữ liệu demo tĩnh (frontend/src/data/fabrics.js). Ba cột này cho phép sản
phẩm vải tạo từ trang admin cũng lọc được:

- products.pattern   : Họa tiết  (VD: Thọ Dơi)  → trang "Lụa Nha Xá thông dụng".
- products.color_tag : Tone màu  (VD: Hồng)     → cả hai trang.
- products.silk_type : Loại lụa                 → trang "Lụa Nha Xá 100% tơ tằm".
"""


def upgrade(db):
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS pattern VARCHAR(80)")
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS color_tag VARCHAR(40)")
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS silk_type VARCHAR(100)")


def downgrade(db):
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS pattern")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS color_tag")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS silk_type")
