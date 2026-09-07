"""
Danh mục quyền của trang admin — nguồn sự thật duy nhất.

Mỗi quyền là một chuỗi "<nhóm>.<thao tác>", nhóm ứng với một tab trong trang
admin. Vai trò (bảng roles) lưu danh sách mã quyền; riêng vai trò toàn quyền
lưu ký tự "*" để tự có mọi quyền thêm mới sau này mà không phải sửa dữ liệu.

Thêm quyền mới: khai báo ở đây → gắn require(...) vào endpoint tương ứng →
trang admin tự hiện thêm ô tick (UI đọc danh mục này qua API).
"""

WILDCARD = "*"

# Có chặn quyền ở API hay không.
#
#   False = phân quyền chỉ để ẩn/hiện trong giao diện admin. API vẫn bắt buộc
#           đăng nhập bằng tài khoản admin, nhưng đã là admin thì gọi thẳng API
#           là làm được mọi thao tác, bất kể vai trò.
#   True  = mỗi endpoint kiểm tra đúng quyền của vai trò và trả 403 nếu thiếu.
#
# Đang để False theo yêu cầu. Đổi thành True là siết lại toàn bộ, không phải
# sửa gì thêm — các endpoint đã khai báo sẵn quyền qua require(...).
ENFORCE_PERMISSIONS = False

PERMISSION_GROUPS = [
    {
        "key": "dashboard",
        "label": "Dashboard",
        "permissions": [
            ("dashboard.view", "Xem tổng quan, doanh thu, số liệu"),
        ],
    },
    {
        "key": "products",
        "label": "Sản phẩm",
        "permissions": [
            ("products.view",   "Xem danh sách & chi tiết sản phẩm"),
            ("products.create", "Thêm sản phẩm mới"),
            ("products.update", "Sửa sản phẩm, ảnh, kích thước"),
            ("products.delete", "Xoá sản phẩm"),
        ],
    },
    {
        "key": "categories",
        "label": "Danh mục",
        "permissions": [
            ("categories.view",   "Xem danh mục & danh mục con"),
            ("categories.create", "Thêm danh mục"),
            ("categories.update", "Sửa danh mục"),
            ("categories.delete", "Xoá danh mục"),
        ],
    },
    {
        "key": "orders",
        "label": "Đơn hàng",
        "permissions": [
            ("orders.view",          "Xem đơn hàng & thông tin khách"),
            ("orders.update_status", "Đổi trạng thái đơn hàng"),
        ],
    },
    {
        "key": "posts",
        "label": "Tin tức",
        "permissions": [
            ("posts.view",   "Xem danh sách bài viết"),
            ("posts.create", "Viết bài mới"),
            ("posts.update", "Sửa bài viết"),
            ("posts.delete", "Xoá bài viết"),
        ],
    },
    {
        "key": "content",
        "label": "Nội dung web",
        "permissions": [
            ("content.view",   "Xem cấu hình nội dung website"),
            ("content.update", "Sửa video trang chủ, hướng dẫn, FAQ, danh sách họa tiết"),
        ],
    },
    {
        "key": "customization",
        "label": "Tuỳ chỉnh sản phẩm",
        "permissions": [
            ("customization.view",   "Xem các mức phụ thu may đo"),
            ("customization.update", "Thêm / sửa / xoá mức phụ thu"),
        ],
    },
    {
        "key": "users",
        "label": "Người dùng",
        "permissions": [
            ("users.view",   "Xem danh sách tài khoản"),
            ("users.create", "Tạo tài khoản"),
            ("users.update", "Sửa tài khoản, đổi mật khẩu, khoá / mở khoá"),
            ("users.delete", "Xoá tài khoản"),
        ],
    },
    {
        "key": "roles",
        "label": "Vai trò & phân quyền",
        "permissions": [
            ("roles.view",   "Xem danh sách vai trò"),
            ("roles.manage", "Tạo / sửa / xoá vai trò và tick quyền"),
        ],
    },
]

ALL_PERMISSIONS: list[str] = [
    code for group in PERMISSION_GROUPS for code, _ in group["permissions"]
]

PERMISSION_LABELS: dict[str, str] = {
    code: label for group in PERMISSION_GROUPS for code, label in group["permissions"]
}


def clean_permissions(codes) -> list[str]:
    """Bỏ mã lạ và mã trùng, giữ nguyên thứ tự khai báo ở trên."""
    if not codes:
        return []
    if WILDCARD in codes:
        return [WILDCARD]
    wanted = set(codes)
    return [code for code in ALL_PERMISSIONS if code in wanted]
