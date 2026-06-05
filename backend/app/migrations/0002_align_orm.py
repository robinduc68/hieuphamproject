"""
Align legacy 0001 schema with current Peewee models (subcategories, product_images,
product_sizes, collections, newsletter table name).
Idempotent where possible for dev DBs.
"""


def upgrade(db):
    db.execute_sql("DROP INDEX IF EXISTS idx_categories_parent")

    db.execute_sql("""
        CREATE TABLE IF NOT EXISTS subcategories (
            id          SERIAL PRIMARY KEY,
            category_id INT          NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
            name        VARCHAR(120) NOT NULL,
            slug        VARCHAR(120) NOT NULL UNIQUE,
            description TEXT,
            image_url   VARCHAR(500),
            is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
            sort_order  INT          NOT NULL DEFAULT 0,
            created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
        )
    """)

    db.execute_sql("""
        INSERT INTO subcategories (category_id, name, slug, description, image_url, is_active, sort_order, created_at, updated_at)
        SELECT c.parent_id, c.name, c.slug, c.description, NULL, c.is_active, c.sort_order::int, c.created_at, c.updated_at
        FROM categories c
        WHERE c.parent_id IS NOT NULL
        ON CONFLICT (slug) DO NOTHING
    """)

    db.execute_sql("""
        UPDATE products p
        SET category_id = c.parent_id
        FROM categories c
        WHERE p.category_id = c.id AND c.parent_id IS NOT NULL
    """)

    db.execute_sql("DELETE FROM categories WHERE parent_id IS NOT NULL")
    db.execute_sql("ALTER TABLE categories DROP COLUMN IF EXISTS parent_id")
    db.execute_sql("ALTER TABLE categories ADD COLUMN IF NOT EXISTS image_url VARCHAR(500)")

    db.execute_sql("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = 'product_images' AND column_name = 'position'
            ) THEN
                ALTER TABLE product_images RENAME COLUMN position TO sort_order;
            END IF;
        END $$
    """)
    db.execute_sql(
        "ALTER TABLE product_images ADD COLUMN IF NOT EXISTS is_primary BOOLEAN NOT NULL DEFAULT FALSE"
    )
    db.execute_sql(
        "ALTER TABLE product_images ALTER COLUMN sort_order TYPE INTEGER USING sort_order::integer"
    )

    db.execute_sql("ALTER TABLE product_sizes ADD COLUMN IF NOT EXISTS stock INT NOT NULL DEFAULT 1")
    db.execute_sql(
        "ALTER TABLE product_sizes ADD COLUMN IF NOT EXISTS is_available BOOLEAN NOT NULL DEFAULT TRUE"
    )
    db.execute_sql("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = 'product_sizes' AND column_name = 'in_stock'
            ) THEN
                UPDATE product_sizes SET is_available = COALESCE(in_stock, TRUE);
                ALTER TABLE product_sizes DROP COLUMN in_stock;
            END IF;
        END $$
    """)

    db.execute_sql(
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS subcategory_id INT REFERENCES subcategories(id) ON DELETE SET NULL"
    )
    db.execute_sql(
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS collection_id INT REFERENCES collections(id) ON DELETE SET NULL"
    )
    db.execute_sql("ALTER TABLE products ADD COLUMN IF NOT EXISTS primary_color VARCHAR(20)")
    db.execute_sql("ALTER TABLE products DROP COLUMN IF EXISTS sub_category")

    db.execute_sql("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = 'collections' AND column_name = 'title'
            ) THEN
                ALTER TABLE collections RENAME COLUMN title TO name;
            END IF;
        END $$
    """)
    db.execute_sql("ALTER TABLE collections ADD COLUMN IF NOT EXISTS cover_url VARCHAR(500)")
    db.execute_sql("ALTER TABLE collections DROP COLUMN IF EXISTS is_tall")
    db.execute_sql("ALTER TABLE collections DROP COLUMN IF EXISTS cover_image")

    db.execute_sql("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'newsletter_subscribers'
            ) AND NOT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'newsletter_subscriptions'
            ) THEN
                ALTER TABLE newsletter_subscribers RENAME TO newsletter_subscriptions;
            END IF;
        END $$
    """)

    db.execute_sql("""
        DROP TRIGGER IF EXISTS trg_subcategories_updated_at ON subcategories;
        CREATE TRIGGER trg_subcategories_updated_at
        BEFORE UPDATE ON subcategories
        FOR EACH ROW EXECUTE FUNCTION set_updated_at()
    """)


def downgrade(db):
    pass
