"""
Migration 0007 – Hai bảng hướng dẫn còn lại ở trang sản phẩm

Trước đây 2 nút "Hướng dẫn lấy số đo & đặt may" và "Hướng dẫn chọn màu & đặt may"
ở trang chi tiết không mở gì cả. Giờ mỗi nút mở một dialog với nội dung soạn ở
trang admin (HTML từ trình soạn thảo, nên có tiêu đề/đậm/nghiêng/ảnh).
"""
import json

DEFAULTS = {
    "measure_guide": {
        "title": "Hướng Dẫn Lấy Số Đo & Đặt May",
        "content": (
            "<h2>Cách lấy số đo</h2>"
            "<p>Dùng thước dây mềm, đo sát người nhưng không siết chặt, mặc đồ mỏng khi đo.</p>"
            "<ul>"
            "<li><strong>Vòng ngực:</strong> đo qua chỗ đầy nhất của ngực, thước song song mặt đất.</li>"
            "<li><strong>Vòng eo:</strong> đo qua chỗ nhỏ nhất của eo.</li>"
            "<li><strong>Vòng mông:</strong> đo qua chỗ nở nhất của mông.</li>"
            "<li><strong>Chiều dài áo:</strong> đo từ chân cổ xuống điểm muốn kết thúc tà áo.</li>"
            "</ul>"
            "<h2>Đặt may theo số đo</h2>"
            "<p>Chọn <em>May theo số đo</em> ở phần hình thức may, sau đó ghi số đo vào ô ghi chú "
            "hoặc gửi cho nhân viên tư vấn qua hotline / fanpage. Chúng tôi sẽ liên hệ xác nhận "
            "trước khi cắt may.</p>"
        ),
    },
    "color_guide": {
        "title": "Hướng Dẫn Chọn Màu & Đặt May",
        "content": (
            "<h2>Chọn màu theo mẫu có sẵn</h2>"
            "<p>Màu hiển thị trên màn hình có thể lệch nhẹ so với vải thật do màn hình và ánh sáng. "
            "Nếu cần chính xác tuyệt đối, liên hệ để được gửi mẫu vải thật.</p>"
            "<h2>Đặt may theo màu riêng</h2>"
            "<p>Chọn <strong>Màu khác</strong> ở phần lựa chọn màu sắc, rồi ghi mã màu hoặc mô tả "
            "màu mong muốn vào ô ghi chú. Nhân viên sẽ liên hệ xác nhận trước khi nhuộm/dệt.</p>"
        ),
    },
}


def upgrade(db):
    for key, value in DEFAULTS.items():
        db.execute_sql(
            "INSERT INTO site_settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING",
            (key, json.dumps(value, ensure_ascii=False)),
        )


def downgrade(db):
    db.execute_sql(
        "DELETE FROM site_settings WHERE key IN ('measure_guide', 'color_guide')"
    )
