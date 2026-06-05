"""
Migration 0001 – Initial schema
Tạo toàn bộ bảng: categories, products, product_images,
product_sizes, collections, users, orders, order_items,
newsletter_subscribers
"""


def upgrade(db):
    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS categories (
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(120)  NOT NULL,
            slug        VARCHAR(120)  NOT NULL UNIQUE,
            description TEXT,
            parent_id   INT           REFERENCES categories(id) ON DELETE SET NULL,
            sort_order  SMALLINT      NOT NULL DEFAULT 0,
            is_active   BOOLEAN       NOT NULL DEFAULT TRUE,
            created_at  TIMESTAMPTZ   NOT NULL DEFAULT now(),
            updated_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id)")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS products (
            id                SERIAL PRIMARY KEY,
            name              VARCHAR(255) NOT NULL,
            slug              VARCHAR(255) NOT NULL UNIQUE,
            price             NUMERIC(14,0) NOT NULL,
            description       TEXT,
            fabric            TEXT,
            care_instructions TEXT,
            shipping_info     TEXT,
            category_id       INT          REFERENCES categories(id) ON DELETE SET NULL,
            sub_category      VARCHAR(120),
            is_new            BOOLEAN      NOT NULL DEFAULT FALSE,
            is_active         BOOLEAN      NOT NULL DEFAULT TRUE,
            is_featured       BOOLEAN      NOT NULL DEFAULT FALSE,
            sort_order        SMALLINT     NOT NULL DEFAULT 0,
            created_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at        TIMESTAMPTZ  NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_products_slug       ON products(slug)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_products_category   ON products(category_id)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_products_is_new     ON products(is_new)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_products_is_featured ON products(is_featured)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_products_is_active  ON products(is_active)")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS product_images (
            id         SERIAL PRIMARY KEY,
            product_id INT          NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            url        VARCHAR(512) NOT NULL,
            color_hex  VARCHAR(10),
            alt_text   VARCHAR(255),
            position   SMALLINT     NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ  NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_pimg_product ON product_images(product_id, position)")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS product_sizes (
            id         SERIAL PRIMARY KEY,
            product_id INT         NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            size       VARCHAR(20) NOT NULL,
            in_stock   BOOLEAN     NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            UNIQUE (product_id, size)
        )
    """)

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS collections (
            id           SERIAL PRIMARY KEY,
            title        VARCHAR(200) NOT NULL,
            subtitle     VARCHAR(200),
            slug         VARCHAR(200) NOT NULL UNIQUE,
            description  TEXT,
            gradient     VARCHAR(300),
            accent_color VARCHAR(10),
            cover_image  VARCHAR(512),
            is_tall      BOOLEAN     NOT NULL DEFAULT FALSE,
            is_active    BOOLEAN     NOT NULL DEFAULT TRUE,
            sort_order   SMALLINT    NOT NULL DEFAULT 0,
            created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS users (
            id              SERIAL PRIMARY KEY,
            email           VARCHAR(255) NOT NULL UNIQUE,
            full_name       VARCHAR(200),
            hashed_password VARCHAR(255) NOT NULL,
            phone           VARCHAR(20),
            address         TEXT,
            is_active       BOOLEAN     NOT NULL DEFAULT TRUE,
            is_admin        BOOLEAN     NOT NULL DEFAULT FALSE,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS orders (
            id            SERIAL PRIMARY KEY,
            user_id       INT          REFERENCES users(id) ON DELETE SET NULL,
            email         VARCHAR(255) NOT NULL,
            full_name     VARCHAR(200) NOT NULL,
            phone         VARCHAR(20)  NOT NULL,
            address       TEXT         NOT NULL,
            city          VARCHAR(100) NOT NULL,
            country       VARCHAR(100) NOT NULL DEFAULT 'Vietnam',
            note          TEXT,
            total         NUMERIC(16,0) NOT NULL,
            status        VARCHAR(20)  NOT NULL DEFAULT 'pending',
            tracking_code VARCHAR(100),
            created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_orders_user   ON orders(user_id)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_orders_email  ON orders(email)")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS order_items (
            id         SERIAL PRIMARY KEY,
            order_id   INT           NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            product_id INT           NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
            size       VARCHAR(20)   NOT NULL,
            quantity   INT           NOT NULL DEFAULT 1,
            price      NUMERIC(14,0) NOT NULL,
            created_at TIMESTAMPTZ   NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ   NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_oitems_order   ON order_items(order_id)")
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_oitems_product ON order_items(product_id)")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id         SERIAL PRIMARY KEY,
            email      VARCHAR(255) NOT NULL UNIQUE,
            full_name  VARCHAR(200),
            is_active  BOOLEAN     NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    db.execute_sql("CREATE INDEX IF NOT EXISTS idx_newsletter_email ON newsletter_subscribers(email)")

    # Trigger: auto-update updated_at
    db.execute_sql("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER LANGUAGE plpgsql AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$
    """)
    for tbl in [
        "categories", "products", "product_images", "product_sizes",
        "collections", "users", "orders", "order_items", "newsletter_subscribers",
    ]:
        db.execute_sql(f"""
            DROP TRIGGER IF EXISTS trg_{tbl}_updated_at ON {tbl};
            CREATE TRIGGER trg_{tbl}_updated_at
            BEFORE UPDATE ON {tbl}
            FOR EACH ROW EXECUTE FUNCTION set_updated_at()
        """)


def downgrade(db):
    for tbl in [
        "newsletter_subscribers", "order_items", "orders",
        "users", "collections", "product_sizes", "product_images",
        "products", "categories",
    ]:
        db.execute_sql(f"DROP TABLE IF EXISTS {tbl} CASCADE")
    db.execute_sql("DROP FUNCTION IF EXISTS set_updated_at CASCADE")
