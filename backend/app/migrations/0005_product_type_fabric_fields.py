"""
Migration 0005 – Phân loại sản phẩm + thông số dành riêng cho vải

- products.product_type : 'apparel' (quần áo) | 'fabric' (vải) → quyết định
  trang chi tiết ngoài web dùng layout nào.
- products.sku_code     : Mã sản phẩm (VD: TD01) — hiện ở khối thông số vải.
- products.specification: Quy cách (VD: 100% Tơ Tằm, chi số tơ 32-33).
- products.fabric_width : Khổ vải (VD: 90cm).
- products.unit_label   : Đơn vị bán (VD: mét) — giá hiển thị "trên 1 <unit>".

Backfill: sản phẩm đang thuộc danh mục "Lụa tơ tằm" (hoặc danh mục con của nó)
được đánh dấu là vải, vì trước đây chưa có field này để phân biệt.
"""


def upgrade(db):
    db.execute_sql(
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS product_type VARCHAR(20) NOT NULL DEFAULT 'apparel'"
    )
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS sku_code VARCHAR(60)")
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS specification TEXT")
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS fabric_width VARCHAR(60)")
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS unit_label VARCHAR(30)")

    # Danh mục vải hiện tại: slug 'lua-to-tam' và các danh mục con của nó.
    db.execute_sql(
        """
        UPDATE products SET product_type = 'fabric'
        WHERE category_id IN (SELECT id FROM categories WHERE slug = 'lua-to-tam')
           OR subcategory_id IN (
                SELECT s.id FROM subcategories s
                JOIN categories c ON c.id = s.category_id
                WHERE c.slug = 'lua-to-tam'
           )
        """
    )


def downgrade(db):
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS product_type")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS sku_code")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS specification")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS fabric_width")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS unit_label")
