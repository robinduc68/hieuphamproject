"""
Migration 0015 – Mã đơn hàng + thanh toán VietQR

Trước đây "mã đơn hàng" hiện ở trang thanh toán là số ngẫu nhiên sinh trong
trình duyệt, không lưu ở đâu cả → khách chuyển khoản xong không đối soát được.
Nay mỗi đơn có order_code thật, dùng luôn làm nội dung chuyển khoản và orderId
gửi sang VietQR.

- orders.order_code        : mã đơn (VD HH000123), duy nhất
- orders.qr_code/qr_link   : mã QR VietQR trả về
- orders.qr_transaction_id : transactionId lúc tạo QR
- orders.payment_ref       : mã giao dịch ngân hàng khi tiền về
- orders.paid_amount/paid_at

Backfill: đơn cũ được gán order_code theo id để không có đơn nào thiếu mã.
"""


def upgrade(db):
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_code VARCHAR(20)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS qr_code TEXT")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS qr_link VARCHAR(500)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS qr_transaction_id VARCHAR(100)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_ref VARCHAR(100)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS paid_amount NUMERIC(16,0)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS paid_at TIMESTAMPTZ")

    db.execute_sql("UPDATE orders SET order_code = 'HH' || LPAD(id::text, 6, '0') WHERE order_code IS NULL")
    db.execute_sql(
        "CREATE UNIQUE INDEX IF NOT EXISTS orders_order_code_uniq ON orders (order_code)"
    )


def downgrade(db):
    db.execute_sql("DROP INDEX IF EXISTS orders_order_code_uniq")
    for col in ("order_code", "qr_code", "qr_link", "qr_transaction_id",
                "payment_ref", "paid_amount", "paid_at"):
        db.execute_sql(f"ALTER TABLE orders DROP COLUMN IF EXISTS {col}")
