"""
Migration 0011 – Danh sách họa tiết của bộ lọc trang vải cho admin sửa

Trước đây danh sách 12 họa tiết nằm cứng trong code (frontend/src/data/fabrics.js
và admin/src/data/fabricOptions.js) nên admin chỉ thêm được họa tiết mới bằng
cách gõ tay, không xoá/sửa được mục có sẵn.

Đưa về site_settings key 'fabric_filters' = {patterns: [...]}:
  - Trang admin "Nội dung web" sửa danh sách.
  - Ô "Họa tiết" trong form sản phẩm chọn từ danh sách này.
  - Sidebar trang "Lụa Nha Xá thông dụng" hiện đúng danh sách này.

Để dạng object (không phải mảng thuần) cho lần sau thêm được tone màu / loại lụa
vào cùng một key mà không phải đổi cấu trúc.
"""
import json

FABRIC_FILTERS = {
    "patterns": [
        "Thọ Dơi", "Đuôi Công", "Cúc", "Cúc Đại Đóa",
        "Sen Tròn", "Sen - Hổ Điệp", "Thủy Tiên", "Phúc Thọ",
        "Long Phụng", "Hoa Mai", "Hoa Đào", "Trúc Mai",
    ],
}


def upgrade(db):
    db.execute_sql(
        "INSERT INTO site_settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING",
        ("fabric_filters", json.dumps(FABRIC_FILTERS, ensure_ascii=False)),
    )

    # Họa tiết admin đã gõ tay cho sản phẩm trước đó → gộp vào danh sách để
    # không mất mục lọc nào đang dùng.
    cursor = db.execute_sql(
        "SELECT DISTINCT pattern FROM products WHERE pattern IS NOT NULL AND pattern <> ''"
    )
    used = [row[0].strip() for row in cursor.fetchall() if row[0] and row[0].strip()]
    if not used:
        return

    cursor = db.execute_sql("SELECT value FROM site_settings WHERE key = %s", ("fabric_filters",))
    row = cursor.fetchone()
    current = json.loads(row[0]) if row and row[0] else {}
    patterns = list(current.get("patterns") or [])
    for p in used:
        if p not in patterns:
            patterns.append(p)
    current["patterns"] = patterns

    db.execute_sql(
        "UPDATE site_settings SET value = %s WHERE key = %s",
        (json.dumps(current, ensure_ascii=False), "fabric_filters"),
    )


def downgrade(db):
    db.execute_sql("DELETE FROM site_settings WHERE key = %s", ("fabric_filters",))
