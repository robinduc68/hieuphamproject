"""
Migration 0004 – Lưu lựa chọn tùy chỉnh per order item
- order_items: thêm tailoring_method, lining_type, color_option (option_key snapshot)
"""


def upgrade(db):
    db.execute_sql(
        "ALTER TABLE order_items ADD COLUMN IF NOT EXISTS tailoring_method VARCHAR(60)"
    )
    db.execute_sql(
        "ALTER TABLE order_items ADD COLUMN IF NOT EXISTS lining_type VARCHAR(60)"
    )
    db.execute_sql(
        "ALTER TABLE order_items ADD COLUMN IF NOT EXISTS color_option VARCHAR(60)"
    )


def downgrade(db):
    db.execute_sql("ALTER TABLE order_items DROP COLUMN IF EXISTS tailoring_method")
    db.execute_sql("ALTER TABLE order_items DROP COLUMN IF EXISTS lining_type")
    db.execute_sql("ALTER TABLE order_items DROP COLUMN IF EXISTS color_option")
