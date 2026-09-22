"""
Migration 0014 – Cho phép số lượng lẻ trong đơn hàng

Vải bán theo mét nên khách hay mua số lẻ (3.8 mét, 2.2 mét). order_items.quantity
đang là INTEGER nên không lưu được; đổi sang NUMERIC(10,2).

Quần áo vẫn đặt theo số nguyên, chỉ là kiểu cột rộng hơn nên chứa được cả hai.
"""


def upgrade(db):
    db.execute_sql(
        "ALTER TABLE order_items ALTER COLUMN quantity TYPE NUMERIC(10,2) "
        "USING quantity::numeric"
    )
    db.execute_sql("ALTER TABLE order_items ALTER COLUMN quantity SET DEFAULT 1")


def downgrade(db):
    # Làm tròn lên số nguyên — đơn vải lẻ sẽ sai số, chỉ dùng khi buộc phải lùi.
    db.execute_sql(
        "ALTER TABLE order_items ALTER COLUMN quantity TYPE INTEGER "
        "USING CEIL(quantity)::integer"
    )
