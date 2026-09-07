"""
Migration 0012 – Vai trò & phân quyền chi tiết cho trang admin

Trước đây chỉ có cờ users.is_admin: đã vào được admin là toàn quyền. Bảng roles
cho phép tạo vai trò (Nhân viên nội dung, Nhân viên đơn hàng…) và tick từng
quyền theo tab / thao tác — danh mục quyền ở app/permissions.py.

- roles.permissions : JSON danh sách mã quyền; ["*"] = toàn quyền.
- roles.is_system   : vai trò gốc, không cho xoá / đổi quyền.
- users.role_id     : vai trò của tài khoản (SET NULL khi vai trò bị xoá).

Backfill: mọi tài khoản is_admin hiện có được gán vai trò "Quản trị viên"
(toàn quyền) để không ai mất quyền sau khi nâng cấp.
"""
import json

FULL_ROLE = "Quản trị viên"

SEED_ROLES = [
    (
        FULL_ROLE,
        "Toàn quyền trên trang quản trị, kể cả quản lý tài khoản và vai trò.",
        ["*"],
        True,
    ),
    (
        "Nhân viên nội dung",
        "Quản lý sản phẩm, danh mục, tin tức và nội dung website. Không xem đơn hàng, doanh thu, tài khoản.",
        [
            "products.view", "products.create", "products.update",
            "categories.view", "categories.update",
            "posts.view", "posts.create", "posts.update",
            "content.view", "content.update",
        ],
        False,
    ),
    (
        "Nhân viên đơn hàng",
        "Xem và xử lý đơn hàng. Chỉ xem sản phẩm, không sửa được nội dung.",
        ["dashboard.view", "orders.view", "orders.update_status", "products.view"],
        False,
    ),
]


def upgrade(db):
    db.execute_sql(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(100) NOT NULL UNIQUE,
            description VARCHAR(255),
            permissions TEXT,
            is_system   BOOLEAN NOT NULL DEFAULT FALSE,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    db.execute_sql(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS role_id INTEGER "
        "REFERENCES roles(id) ON DELETE SET NULL"
    )

    for name, description, permissions, is_system in SEED_ROLES:
        db.execute_sql(
            """
            INSERT INTO roles (name, description, permissions, is_system)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            """,
            (name, description, json.dumps(permissions, ensure_ascii=False), is_system),
        )

    # Admin đang có → vai trò toàn quyền, giữ nguyên khả năng thao tác cũ.
    db.execute_sql(
        """
        UPDATE users SET role_id = (SELECT id FROM roles WHERE name = %s)
        WHERE is_admin = TRUE AND role_id IS NULL
        """,
        (FULL_ROLE,),
    )


def downgrade(db):
    db.execute_sql("ALTER TABLE users DROP COLUMN IF EXISTS role_id")
    db.execute_sql("DROP TABLE IF EXISTS roles")
