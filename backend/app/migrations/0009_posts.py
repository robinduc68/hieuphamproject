"""
Migration 0009 – Bảng bài viết cho trang "Tin tức"

Trước đây danh sách tin tức và nội dung từng bài nằm cứng trong code frontend
(NewsView.vue / NewsDetailView.vue) nên admin không sửa được. Bảng này đưa
toàn bộ nội dung đó về DB, quản lý trong trang admin (mục "Tin tức").

Seed: 6 bài đang hiển thị ngoài website được đưa vào để không mất nội dung —
admin sửa/xoá lại tuỳ ý. Chỉ chạy khi bảng còn trống.
"""

SEED = [
    dict(
        slug="da-ngam-hop-voi-mau-gi",
        tag="Tips mặc đẹp",
        published_at="2025-08-08",
        cover_color="linear-gradient(135deg, #C8A898 0%, #B08878 50%, #D0B0A0 100%)",
        title='Da ngăm hợp với màu gì? 7 gam màu "cứ mặc là đẹp"',
        subtitle="Khám phá bảng màu được các chuyên gia thời trang gợi ý dành riêng cho tông da ngăm — đẹp tự nhiên, không cần cố.",
        excerpt="Khám phá bảng màu được các chuyên gia thời trang gợi ý dành riêng cho tông da ngăm.",
        content="""
<p>Da ngăm vốn được ví như "vàng nâu" của người Việt — ấm áp, khỏe khoắn và đậm chất nhiệt đới. Thế nhưng nhiều người vẫn loay hoay không biết chọn màu sắc như thế nào để tôn lên làn da này. Dưới đây là 7 gam màu mà các chuyên gia phong cách khuyên bạn nên thử.</p>
<h2>1. Màu trắng ngà (off-white)</h2>
<p>Không phải trắng tinh, mà là trắng kem hoặc trắng ngà mới là lựa chọn hoàn hảo. Gam màu này tạo ra sự tương phản nhẹ nhàng, làm nổi bật làn da ngăm mà không gây cảm giác "lạc lõng".</p>
<h2>2. Vàng đất &amp; caramel</h2>
<p>Các tông vàng ấm như caramel, vàng mustard hay vàng đất đều cực kỳ hợp với da ngăm. Chúng cùng hệ màu ấm nên hòa hợp tự nhiên, tạo cảm giác gương mặt rạng rỡ hơn.</p>
<ul>
<li><strong>Vàng mustard</strong> — đậm, cá tính, hợp với áo dài cách điệu.</li>
<li><strong>Caramel nhạt</strong> — thanh lịch, phù hợp với áo dài truyền thống.</li>
<li><strong>Vàng đất</strong> — gần với màu đất nung, đậm chất Á Đông.</li>
</ul>
<h2>3. Đỏ rượu &amp; đỏ gạch</h2>
<p>Đây là bộ đôi "không bao giờ sai" cho làn da ngăm. Đỏ rượu tạo nên vẻ sang trọng, huyền bí; đỏ gạch mang lại cảm giác ấm áp, gần gũi nhưng vẫn đủ nổi bật.</p>
<h2>4. Xanh cổ vịt &amp; xanh ngọc</h2>
<p>Các tông xanh lạnh khi chạm vào da ngăm lại tạo ra hiệu ứng tương phản rất đẹp mắt. Xanh cổ vịt hay xanh ngọc đều mang lại vẻ thanh thoát, hiện đại cho người mặc.</p>
<h2>5. Cam san hô</h2>
<p>Cam san hô — màu xu hướng nhiều năm liền — là người bạn đồng hành lý tưởng của làn da ngăm. Màu này "ăn" với da ngăm theo cách không một gam màu nào sánh được.</p>
<h2>6. Hồng đất &amp; hồng nâu</h2>
<p>Hồng đất (mauve) hay hồng nâu (dusty rose) là những gam màu tinh tế, không quá chói, tôn lên vẻ nữ tính mà vẫn giữ được nét thanh lịch đặc trưng của áo dài.</p>
<h2>7. Tím mận &amp; tím eggplant</h2>
<p>Cuối danh sách nhưng không hề kém cạnh — tím mận và tím tối mang lại vẻ quý phái, bí ẩn. Khi kết hợp với chất liệu lụa tơ tằm có ánh nhũ, hiệu ứng đẹp đến khó tin.</p>
<blockquote>"Màu sắc là ngôn ngữ riêng của áo dài — mỗi gam màu kể một câu chuyện khác nhau về người mặc nó."</blockquote>
<p>Dù bạn chọn gam màu nào, điều quan trọng nhất vẫn là sự tự tin của người mặc. Hà Hoạt Silk luôn sẵn sàng tư vấn và đồng hành cùng bạn trên hành trình tìm kiếm bộ áo dài ưng ý nhất.</p>
""",
    ),
    dict(
        slug="cach-chon-vai-lua-chuan",
        tag="Kiến thức vải",
        published_at="2025-08-01",
        cover_color="linear-gradient(135deg, #A8B8C8 0%, #8898A8 50%, #B8C8D8 100%)",
        title='Cách chọn vải lụa chuẩn — không bị "hớ" khi mua online',
        subtitle="Phân biệt lụa tơ tằm thật với các loại vải giả lụa tràn lan trên thị trường.",
        excerpt="Phân biệt lụa tơ tằm thật với các loại vải giả lụa tràn lan trên thị trường hiện nay...",
        content="""
<p>Thị trường vải hiện nay vô cùng đa dạng, khiến không ít người khó phân biệt lụa thật và lụa giả. Bài viết này sẽ giúp bạn trang bị những kiến thức cần thiết.</p>
<blockquote>"Lụa thật không bao giờ cần quảng cáo — chất liệu tự nói lên tất cả."</blockquote>
<p>Khi mua vải lụa, hãy luôn yêu cầu thông tin xuất xứ và chứng nhận chất lượng từ nhà cung cấp.</p>
""",
    ),
    dict(
        slug="ao-dai-cho-mua-cuoi",
        tag="Xu hướng",
        published_at="2025-07-25",
        cover_color="linear-gradient(135deg, #D4C8A8 0%, #C4B890 50%, #D8C8A8 100%)",
        title="Áo dài cho mùa cưới 2025 — xu hướng màu sắc và họa tiết",
        subtitle="Điểm qua những thiết kế áo dài đang được săn đón nhất trong mùa cưới năm nay.",
        excerpt="Điểm qua những thiết kế áo dài đang được săn đón nhất trong mùa cưới năm nay...",
        content="""
<p>Mùa cưới 2025 đang đến gần với những xu hướng áo dài mới mẻ, kết hợp giữa truyền thống và hiện đại.</p>
<blockquote>"Áo dài cưới không chỉ là trang phục — đó là ký ức được dệt bằng lụa."</blockquote>
<p>Liên hệ với Hà Hoạt Silk để được tư vấn và may bộ áo dài cưới hoàn hảo nhất.</p>
""",
    ),
    dict(
        slug="bao-quan-ao-dai-lua",
        tag="Chăm sóc",
        published_at="2025-07-18",
        cover_color="linear-gradient(135deg, #C8D0A8 0%, #B8C098 50%, #D0D8B0 100%)",
        title="Bí quyết bảo quản áo dài lụa bền đẹp qua năm tháng",
        subtitle="Những lưu ý quan trọng giúp áo dài lụa tơ tằm luôn giữ được độ bóng và form dáng.",
        excerpt="Những lưu ý quan trọng giúp áo dài lụa tơ tằm luôn giữ được độ bóng và form dáng...",
        content="""
<p>Áo dài lụa tơ tằm nên được giặt khô để giữ độ bóng và hình dạng tốt nhất. Tránh giặt máy, vắt xoắn hoặc phơi dưới ánh nắng trực tiếp.</p>
<p>Khi cất giữ, hãy treo thẳng hoặc gấp nhẹ nhàng, bảo quản nơi thoáng mát, tránh ẩm mốc.</p>
""",
    ),
    dict(
        slug="lua-to-tam-va-suc-khoe",
        tag="Kiến thức vải",
        published_at="2025-07-10",
        cover_color="linear-gradient(135deg, #D0B8C8 0%, #C0A0B0 50%, #D8C0C8 100%)",
        title="Lụa tơ tằm và sức khoẻ — lý do người xưa chuộng dùng",
        subtitle="Khoa học hiện đại chứng minh lụa tơ tằm có nhiều lợi ích vượt trội cho làn da.",
        excerpt="Khoa học hiện đại chứng minh lụa tơ tằm có nhiều lợi ích vượt trội cho làn da...",
        content="""
<p>Lụa tơ tằm là sợi protein tự nhiên, thoáng khí và ít gây kích ứng — lý do người xưa chuộng dùng cho trang phục mặc sát người.</p>
""",
    ),
    dict(
        slug="phong-cach-ao-dai-hien-dai",
        tag="Phong cách",
        published_at="2025-07-02",
        cover_color="linear-gradient(135deg, #B8C8D8 0%, #A0B0C0 50%, #C0D0E0 100%)",
        title="Phong cách áo dài hiện đại — giữa giữ hồn và đổi mới",
        subtitle="Áo dài đang được tái sinh với ngôn ngữ thiết kế mới mà vẫn giữ được bản sắc dân tộc.",
        excerpt="Áo dài đang được tái sinh với ngôn ngữ thiết kế mới mà vẫn giữ được bản sắc dân tộc...",
        content="""
<p>Áo dài đang được tái sinh với ngôn ngữ thiết kế mới — phom dáng gọn hơn, hoạ tiết tối giản hơn — mà vẫn giữ được bản sắc dân tộc.</p>
""",
    ),
]


def upgrade(db):
    db.execute_sql(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id           SERIAL PRIMARY KEY,
            title        VARCHAR(255) NOT NULL,
            slug         VARCHAR(255) NOT NULL UNIQUE,
            tag          VARCHAR(80),
            subtitle     TEXT,
            excerpt      TEXT,
            content      TEXT,
            cover_image  VARCHAR(500),
            cover_color  VARCHAR(120),
            published_at DATE,
            is_published BOOLEAN NOT NULL DEFAULT TRUE,
            sort_order   INTEGER NOT NULL DEFAULT 0,
            created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    cursor = db.execute_sql("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0]:
        return   # đã có bài viết → không seed đè

    for i, p in enumerate(SEED):
        db.execute_sql(
            """
            INSERT INTO posts
                (title, slug, tag, subtitle, excerpt, content, cover_color, published_at, sort_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO NOTHING
            """,
            (
                p["title"], p["slug"], p["tag"], p["subtitle"], p["excerpt"],
                p["content"].strip(), p["cover_color"], p["published_at"], i,
            ),
        )


def downgrade(db):
    db.execute_sql("DROP TABLE IF EXISTS posts")
