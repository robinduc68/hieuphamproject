"""
Migration 0006 – Bảng cấu hình nội dung website (admin sửa được)

Các key khởi tạo:
  - hero_video            : video nền đầu trang chủ (url + poster)
  - size_guide            : bảng "Hướng dẫn chọn size" ở trang sản phẩm
  - fabric_tailoring_guide: bảng "Định mức may đo" ở trang vải

`value` là JSON chuỗi. Bảng dạng {columns: [...], rows: [[...], ...]} nên admin
thêm/bớt cột và dòng tuỳ ý mà không phải đổi schema.
"""
import json

DEFAULTS = {
    "hero_video": {
        "url": "/videos/hero.webm",
        "poster": "/videos/hero-poster.jpg",
    },
    "size_guide": {
        "title": "Hướng Dẫn Chọn Size",
        "note": "* Số đo tính theo cm. Nếu số đo nằm giữa 2 size, chọn size lớn hơn.",
        "columns": ["Size", "Ngực (cm)", "Eo (cm)", "Hông (cm)", "Chiều cao (cm)"],
        "rows": [
            ["32", "76–80",   "60–64", "84–88",   "150–155"],
            ["34", "81–85",   "65–69", "89–93",   "153–158"],
            ["36", "86–90",   "70–74", "94–98",   "156–161"],
            ["38", "91–95",   "75–79", "99–103",  "158–163"],
            ["40", "96–100",  "80–84", "104–108", "160–165"],
            ["42", "101–106", "85–90", "109–114", "162–167"],
        ],
    },
    "fabric_tailoring_guide": {
        "title": "Định Mức May Đo",
        "note": "* Định mức tham khảo với khổ vải 90cm. Số đo lớn hoặc kiểu dáng cầu kỳ có thể cần thêm vải.",
        "columns": ["Sản phẩm", "Chiều cao", "Định mức vải (mét)"],
        "rows": [
            ["Áo dài 2 tà", "Dưới 1m60",    "2.4 – 2.6"],
            ["Áo dài 2 tà", "1m60 – 1m70",  "2.6 – 2.8"],
            ["Áo dài 4 tà", "Dưới 1m60",    "2.8 – 3.0"],
            ["Áo dài 4 tà", "1m60 – 1m70",  "3.0 – 3.2"],
            ["Pháp phục",   "Mọi chiều cao", "3.0 – 3.5"],
            ["Quần lụa",    "Mọi chiều cao", "1.6 – 1.8"],
        ],
    },
}


def upgrade(db):
    db.execute_sql(
        """
        CREATE TABLE IF NOT EXISTS site_settings (
            id         SERIAL PRIMARY KEY,
            key        VARCHAR(80) NOT NULL UNIQUE,
            value      TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    for key, value in DEFAULTS.items():
        db.execute_sql(
            "INSERT INTO site_settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING",
            (key, json.dumps(value, ensure_ascii=False)),
        )


def downgrade(db):
    db.execute_sql("DROP TABLE IF EXISTS site_settings")
