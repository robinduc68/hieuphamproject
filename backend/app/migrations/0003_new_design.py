"""
Migration 0003 – New design
- orders: thêm payment_method, payment_status, shipping_fee, discount_amount,
          discount_code, grand_total, district, ward
- order_items: thêm product_name (snapshot), đổi product FK từ RESTRICT → SET NULL
- product_sizes: thêm sort_order
- products: thêm compare_at_price
- customization_options: bảng mới (global options + giá điều chỉnh)
"""


def upgrade(db):
    # ── products ──────────────────────────────────────────────────────────
    db.execute_sql(
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS compare_at_price NUMERIC(14,0)"
    )

    # ── product_sizes ─────────────────────────────────────────────────────
    db.execute_sql(
        "ALTER TABLE product_sizes ADD COLUMN IF NOT EXISTS sort_order SMALLINT NOT NULL DEFAULT 0"
    )

    # ── orders: các trường mới ────────────────────────────────────────────
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS ward             VARCHAR(100)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS district         VARCHAR(100)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method   VARCHAR(30)   NOT NULL DEFAULT 'cod'")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_status   VARCHAR(20)   NOT NULL DEFAULT 'unpaid'")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_fee     NUMERIC(16,0) NOT NULL DEFAULT 0")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS discount_amount  NUMERIC(16,0) NOT NULL DEFAULT 0")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS discount_code    VARCHAR(50)")
    db.execute_sql("ALTER TABLE orders ADD COLUMN IF NOT EXISTS grand_total      NUMERIC(16,0)")
    # backfill grand_total = total cho rows cũ
    db.execute_sql("UPDATE orders SET grand_total = total WHERE grand_total IS NULL")
    db.execute_sql("ALTER TABLE orders ALTER COLUMN grand_total SET NOT NULL")
    db.execute_sql("ALTER TABLE orders ALTER COLUMN grand_total SET DEFAULT 0")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status)")

    # ── order_items: snapshot product_name ────────────────────────────────
    db.execute_sql(
        "ALTER TABLE order_items ADD COLUMN IF NOT EXISTS product_name VARCHAR(255)"
    )
    # backfill tên sản phẩm cho rows cũ
    db.execute_sql("""
        UPDATE order_items oi
        SET product_name = p.name
        FROM products p
        WHERE oi.product_id = p.id AND oi.product_name IS NULL
    """)

    # đổi FK product_id từ RESTRICT → SET NULL
    db.execute_sql("""
        DO $$
        DECLARE _cname TEXT;
        BEGIN
            SELECT conname INTO _cname
            FROM pg_constraint
            WHERE conrelid = 'order_items'::regclass
              AND contype  = 'f'
              AND confrelid = 'products'::regclass;
            IF _cname IS NOT NULL THEN
                EXECUTE 'ALTER TABLE order_items DROP CONSTRAINT ' || _cname;
            END IF;
        END $$
    """)
    db.execute_sql("""
        ALTER TABLE order_items
        ADD CONSTRAINT order_items_product_id_fkey
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
    """)

    # ── customization_options ─────────────────────────────────────────────
    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS customization_options (
            id               SERIAL        PRIMARY KEY,
            group_key        VARCHAR(60)   NOT NULL,
            group_label      VARCHAR(120)  NOT NULL,
            option_key       VARCHAR(60)   NOT NULL,
            option_label     VARCHAR(120)  NOT NULL,
            price_adjustment NUMERIC(14,0) NOT NULL DEFAULT 0,
            sort_order       SMALLINT      NOT NULL DEFAULT 0,
            is_active        BOOLEAN       NOT NULL DEFAULT TRUE,
            created_at       TIMESTAMPTZ   NOT NULL DEFAULT now(),
            updated_at       TIMESTAMPTZ   NOT NULL DEFAULT now(),
            UNIQUE (group_key, option_key)
        )
    """)
    db.execute_sql(
        "CREATE INDEX IF NOT EXISTS idx_custopts_group ON customization_options(group_key, sort_order)"
    )
    db.execute_sql("""
        DROP TRIGGER IF EXISTS trg_customization_options_updated_at ON customization_options;
        CREATE TRIGGER trg_customization_options_updated_at
        BEFORE UPDATE ON customization_options
        FOR EACH ROW EXECUTE FUNCTION set_updated_at()
    """)

    # seed dữ liệu mặc định
    db.execute_sql("""
        INSERT INTO customization_options
            (group_key, group_label, option_key, option_label, price_adjustment, sort_order)
        VALUES
            ('tailoring_method', 'Hình thức may', 'size',         'May theo size',      0,      0),
            ('tailoring_method', 'Hình thức may', 'custom',       'May theo số đo',     500000, 1),
            ('lining_type',      'Tà trong',       'lien_ta',      'May liền tà ngoài',  0,      0),
            ('lining_type',      'Tà trong',       'yem_roi',      'May yếm rời',         300000, 1),
            ('color_option',     'Màu sắc',        'same',         'Giống ảnh mẫu',      0,      0),
            ('color_option',     'Màu sắc',        'custom_color', 'Phối màu riêng',     200000, 1)
        ON CONFLICT (group_key, option_key) DO NOTHING
    """)


def downgrade(db):
    db.execute_sql("DROP TABLE IF EXISTS customization_options CASCADE")
    db.execute_sql("ALTER TABLE order_items DROP COLUMN IF EXISTS product_name")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS ward")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS district")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS payment_method")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS payment_status")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS shipping_fee")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS discount_amount")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS discount_code")
    db.execute_sql("ALTER TABLE orders DROP COLUMN IF EXISTS grand_total")
    db.execute_sql("ALTER TABLE product_sizes DROP COLUMN IF EXISTS sort_order")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS compare_at_price")
