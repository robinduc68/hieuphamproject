"""
Cây danh mục sản phẩm — nguồn sự thật duy nhất.

Dùng bởi:
  - app/seed.py                 (seed lần đầu khi DB trống)
  - scripts/seed_categories.py  (đồng bộ lại trên DB đã có dữ liệu)

Đây phải khớp với menu "Sản phẩm" ngoài website. Frontend lấy danh mục từ
API /api/categories/ nên sửa ở đây (hoặc thêm trong trang admin) là menu đổi theo.
"""

# (slug, tên, [(slug con, tên con), ...])
TAXONOMY = [
    ("ao-dai", "Áo dài", [
        ("ao-dai-2-ta",     "Áo dài 2 tà"),
        ("ao-dai-4-ta",     "Áo dài 4 tà"),
        ("ao-dai-theu-tay", "Áo dài thêu tay"),
    ]),
    ("phap-phuc", "Pháp phục", []),
    ("dam-lua",   "Đầm lụa",   []),
    ("khan-lua", "Khăn lụa", [
        ("khan-lua-ve-tay-cao-cap",    "Khăn lụa vẽ tay cao cấp"),
        ("khan-lua-loang-tia-cao-cap", "Khăn lụa loang tia cao cấp"),
        ("khan-lua-tron-cao-cap",      "Khăn lụa trơn cao cấp"),
    ]),
    ("lua-to-tam", "Lụa tơ tằm", []),
]

# Danh mục của bộ dữ liệu demo cũ, đã bỏ. Giữ lại để script đồng bộ biết
# cái nào cần dọn / chuyển sản phẩm đi.
LEGACY_SLUGS = ["modern-heritage", "womenswear", "menswear"]

# Sản phẩm demo trong app/seed.py vẫn ghi danh mục con theo tên cũ →
# quy về danh mục cha mới. Danh mục con để trống, admin tự chọn lại.
LEGACY_PRODUCT_CATEGORY = {
    "ao-dai-madame":         "ao-dai",
    "ao-dai-firstlady":      "ao-dai",
    "ao-ba-ba-mademoiselle": "ao-dai",
    "ba-ba-gabriella":       "ao-dai",
}
