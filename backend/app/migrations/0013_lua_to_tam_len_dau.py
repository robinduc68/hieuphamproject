"""
Migration 0013 – Đưa danh mục "Lụa tơ tằm" lên đầu menu

Thứ tự menu Sản phẩm ngoài website lấy theo categories.sort_order. Trước đây
"Lụa tơ tằm" nằm cuối; migration này đẩy nó lên đầu một lần theo yêu cầu.

Từ nay admin tự sắp xếp được bằng nút ↑ ↓ ở trang Danh mục, nên không cần
thêm migration nào khác cho việc đổi thứ tự.
"""

SLUG = "lua-to-tam"


def upgrade(db):
    cursor = db.execute_sql("SELECT id, sort_order FROM categories WHERE slug = %s", (SLUG,))
    row = cursor.fetchone()
    if row is None:
        return                      # DB chưa có danh mục này → bỏ qua
    if row[1] == 0:
        return                      # đã ở đầu rồi

    # Đẩy các danh mục khác xuống 1 bậc, giữ nguyên thứ tự tương đối giữa chúng
    db.execute_sql("UPDATE categories SET sort_order = sort_order + 1 WHERE slug <> %s", (SLUG,))
    db.execute_sql("UPDATE categories SET sort_order = 0 WHERE slug = %s", (SLUG,))


def downgrade(db):
    # Thứ tự cũ là dữ liệu do người dùng chỉnh, không khôi phục tự động được.
    pass
