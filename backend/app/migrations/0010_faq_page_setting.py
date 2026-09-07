"""
Migration 0010 – Nội dung trang "Câu hỏi thường gặp" cho admin sửa

Trước đây danh sách câu hỏi nằm cứng trong frontend/src/views/FaqView.vue.
Đưa về site_settings key 'faq_page' = {title, items: [{question, answer}]},
admin sửa trong trang "Nội dung web".
"""
import json

FAQ_PAGE = {
    "title": "CÂU HỎI THƯỜNG GẶP",
    "items": [
        {
            "question": "Mất bao lâu để hoàn thành một sản phẩm may đo?",
            "answer": "Trung bình, quy trình may đo thủ công sẽ mất từ 1–2 tuần kể từ khi bạn chốt đơn hàng và đặt cọc. Mọi đường kim mũi chỉ đều cần tính toán tỉ mỉ để phù hợp với bạn nhất, Hà Hoạt Silk hy vọng bạn có thể kiên nhẫn chờ đợi tác phẩm của mình.",
        },
        {
            "question": "Sản phẩm thực tế có hoàn toàn giống ảnh không?",
            "answer": "Màu sắc thực tế có thể chênh lệch nhẹ so với ảnh chụp do điều kiện ánh sáng và hiển thị màn hình. Tuy nhiên chất liệu, họa tiết và đường may đều được thực hiện chính xác theo mẫu. Nếu cần, bạn có thể yêu cầu gửi ảnh vải thực tế trước khi đặt hàng.",
        },
        {
            "question": "Tôi có thể đặt may theo số đo riêng không?",
            "answer": "Hoàn toàn có thể. Hà Hoạt Silk nhận may theo số đo cá nhân với đầy đủ các thông số: ngực, eo, hông, chiều dài tay, chiều cao. Bạn có thể tham khảo hướng dẫn lấy số đo trên trang hoặc liên hệ trực tiếp để được hỗ trợ.",
        },
        {
            "question": "Chính sách đổi trả như thế nào?",
            "answer": "Hà Hoạt Silk hỗ trợ đổi trả trong vòng 7 ngày kể từ ngày nhận hàng với điều kiện sản phẩm chưa qua sử dụng, còn nguyên tag và bao bì. Riêng sản phẩm may theo số đo cá nhân sẽ không áp dụng đổi trả, ngoại trừ trường hợp lỗi từ phía nhà sản xuất.",
        },
        {
            "question": "Hà Hoạt Silk có giao hàng quốc tế không?",
            "answer": "Có, chúng tôi giao hàng đến hơn 30 quốc gia. Thời gian giao hàng quốc tế từ 7–14 ngày làm việc tùy khu vực. Phí vận chuyển sẽ được tính dựa trên địa chỉ nhận hàng và trọng lượng đơn hàng.",
        },
        {
            "question": "Tôi cần đặt cọc bao nhiêu khi đặt may?",
            "answer": "Khi đặt may, bạn cần thanh toán trước 50% giá trị đơn hàng để xác nhận. Phần còn lại sẽ được thanh toán khi sản phẩm hoàn thành và trước khi giao hàng. Chúng tôi chấp nhận thanh toán qua chuyển khoản ngân hàng, MoMo và các ví điện tử phổ biến.",
        },
        {
            "question": "Làm thế nào để bảo quản áo dài lụa tơ tằm?",
            "answer": "Áo dài lụa tơ tằm nên được giặt khô (dry clean only) để giữ độ bóng và hình dạng tốt nhất. Tránh giặt máy, vắt xoắn hoặc phơi dưới ánh nắng trực tiếp. Khi cất giữ, hãy treo thẳng hoặc gấp nhẹ nhàng, bảo quản nơi thoáng mát, tránh ẩm mốc.",
        },
    ],
}


def upgrade(db):
    db.execute_sql(
        "INSERT INTO site_settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING",
        ("faq_page", json.dumps(FAQ_PAGE, ensure_ascii=False)),
    )


def downgrade(db):
    db.execute_sql("DELETE FROM site_settings WHERE key = %s", ("faq_page",))
