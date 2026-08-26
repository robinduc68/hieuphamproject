"""
Seed script – chạy 1 lần khi DB trống.
Chạy: python -m app.seed
"""
import sys
from decimal import Decimal
from app.database import db
from app.models.category   import Category, SubCategory
from app.models.product   import Product, ProductImage, ProductSize
from app.models.collection import Collection
from app.models.user       import User
from app.auth              import hash_password
from app.taxonomy          import TAXONOMY, LEGACY_PRODUCT_CATEGORY

# ── Products ──────────────────────────────────────────────────────────────
PRODUCTS = [
    # ── Áo Dài Madame ────────────────────────────────────────────────────
    {
        "name": "Vàng Kim Hoàng – Lập Xuân",
        "slug": "vang-kim-hoang-lap-xuan",
        "price": 12_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Lập Xuân",
        "is_new": True,
        "is_featured": False,
        "sort_order": 0,
        "color_hex": "#c9a227",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Bảng màu Vàng Kim Hoàng lấy cảm hứng từ sắc vàng rực rỡ của mùa xuân sang trọng, "
            "mang đến vẻ đẹp quý phái và đầy sức sống. Màu sắc ấm áp, tươi sáng gợi lên tinh "
            "thần phồn thịnh và hy vọng của tiết Lập Xuân.\n\n"
            "Vàng Kim Hoàng là màu của sự thịnh vượng và thanh tao, không lòe loẹt mà vẫn đủ "
            "sức thu hút và nổi bật trong từng khoảnh khắc."
        ),
        "fabric": "Lụa Mỹ Ngọc dệt tay từ làng nghề Vạn Phúc, Hà Đông. Độ mềm mại cao, thoáng khí, không nhăn sau khi giặt nhẹ.",
        "care_instructions": "Giặt tay nhẹ nhàng với nước mát. Không dùng máy giặt. Phơi nơi thoáng mát, tránh ánh nắng trực tiếp. Là ủi ở nhiệt độ thấp với khăn lót.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày kể từ ngày nhận hàng.",
    },
    {
        "name": "Purple Sky – Y Vân Thưởng",
        "slug": "purple-sky-y-van-thuong",
        "price": 12_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Y Vân Thưởng",
        "is_new": False,
        "is_featured": False,
        "sort_order": 1,
        "color_hex": "#7b5ea7",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Sắc tím Purple Sky gợi lên vẻ đẹp huyền bí của bầu trời hoàng hôn, kết hợp giữa "
            "tím lavender thanh nhã và tím sâu sang trọng.\n\n"
            "Purple Sky thuộc dòng Y Vân Thưởng – bộ sưu tập lấy cảm hứng từ các điệu dân ca "
            "Việt Nam cổ truyền, mỗi chiếc áo là một tác phẩm nghệ thuật mang đậm bản sắc Đông Dương."
        ),
        "fabric": "Gấm lụa tơ tằm tự nhiên 100%, dệt nổi hoa văn truyền thống. Nhập từ làng nghề Mã Châu, Quảng Nam.",
        "care_instructions": "Giặt khô hoặc giặt tay cẩn thận với nước lạnh. Bảo quản trong túi vải thoáng khí.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Crimson Fuchsia – Y Vân Thưởng",
        "slug": "crimson-fuchsia-y-van-thuong",
        "price": 12_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Y Vân Thưởng",
        "is_new": False,
        "is_featured": False,
        "sort_order": 2,
        "color_hex": "#c0395a",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Crimson Fuchsia – sự giao thoa giữa đỏ thẫm và hồng fuchsia rực rỡ, tạo nên tông "
            "màu táo bạo nhưng vẫn giữ được sự tinh tế đặc trưng của HUY VO.\n\n"
            "Màu sắc mang năng lượng mạnh mẽ, tự tin và kiêu sa – lý tưởng cho những dịp lễ trọng."
        ),
        "fabric": "Lụa Charmeuse cao cấp nhập khẩu, bề mặt bóng mượt, rủ tự nhiên theo đường cơ thể.",
        "care_instructions": "Giặt tay với nước lạnh, xà phòng trung tính. Vắt nhẹ, không vắt xoắn.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Xanh Ngọc Phỉ – Y Vân Thưởng",
        "slug": "xanh-ngoc-phi-y-van-thuong",
        "price": 26_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Y Vân Thưởng",
        "is_new": False,
        "is_featured": False,
        "sort_order": 3,
        "color_hex": "#2e8b7a",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Xanh Ngọc Phỉ lấy cảm hứng từ sắc xanh của ngọc phỉ thúy – loại đá quý biểu trưng "
            "cho sự thanh cao và trường thọ trong văn hóa Á Đông.\n\n"
            "Sản phẩm thuộc phân khúc cao cấp nhất của dòng Y Vân Thưởng, được thêu tay hoàn toàn "
            "bởi nghệ nhân làng Quất Động."
        ),
        "fabric": "Nhung tơ tằm thêu tay 100%. Hoa văn thêu nổi theo kỹ thuật truyền thống làng Quất Động, Thường Tín.",
        "care_instructions": "Chỉ giặt khô (Dry Clean Only). Bảo quản trong túi vải tối màu, tránh ánh sáng.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Hồng Sakura – Lập Xuân",
        "slug": "hong-sakura-lap-xuan",
        "price": 12_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Lập Xuân",
        "is_new": False,
        "is_featured": False,
        "sort_order": 4,
        "color_hex": "#e8a0b4",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Hồng Sakura thuộc bộ sưu tập Lập Xuân, lấy cảm hứng từ sắc hoa anh đào nhẹ nhàng, "
            "tinh khôi. Tông hồng pastel dịu dàng mang đến cảm giác trong sáng và nữ tính.\n\n"
            "Màu Hồng Sakura phù hợp với nhiều loại da và dễ phối đồ cho cả những buổi sáng xuân "
            "sang trọng lẫn các dịp lễ tết."
        ),
        "fabric": "Lụa Hà Đông dệt thủ công, nhuộm màu tự nhiên từ chiết xuất hoa hồng.",
        "care_instructions": "Giặt tay nhẹ với nước mát. Dùng nước xả vải để giữ màu. Không dùng thuốc tẩy.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Đỏ Ngự – Tradition",
        "slug": "do-ngu-tradition",
        "price": 10_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Tradition",
        "is_new": False,
        "is_featured": False,
        "sort_order": 5,
        "color_hex": "#8b1a2a",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Đỏ Ngự – màu đỏ của cung đình Huế xưa, mang trên mình trọng trách văn hóa và ký ức "
            "lịch sử. Đây là sắc đỏ sâu thẫm, không chói gắt mà ấm áp như ánh lửa.\n\n"
            "Dòng Tradition của HUY VO là sự tôn vinh thuần túy nhất cho áo dài cổ điển – phom "
            "dáng giữ nguyên vẹn theo kiểu truyền thống, không can thiệp bởi xu hướng đương đại."
        ),
        "fabric": "Lụa Bảo Lộc cao cấp, nhuộm đỏ bằng kỹ thuật nhuộm cổ truyền của làng dệt Mỹ Đức.",
        "care_instructions": "Giặt tay riêng vì màu đậm có thể phai nhẹ lần đầu. Dùng nước lạnh. Phơi trong bóng râm.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Hoàng Lưu Ly – Y Vân Thưởng",
        "slug": "hoang-luu-ly",
        "price": 26_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Y Vân Thưởng",
        "is_new": False,
        "is_featured": False,
        "sort_order": 6,
        "color_hex": "#d4a017",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Hoàng Lưu Ly – sắc vàng của lưu ly quý giá, gợi lên hình ảnh những trang sức cổ vật "
            "trong cung đình. Tông vàng amber sâu pha ánh lục huyền ảo tạo nên chiều sâu thị giác.\n\n"
            "Sản phẩm cao cấp nhất trong dòng Y Vân Thưởng, kết hợp thêu tay và đính hạt tay bởi "
            "các nghệ nhân với hơn 20 năm kinh nghiệm."
        ),
        "fabric": "Gấm Thành Mỹ dệt kim tuyến vàng, đính kèm hạt cườm Séc và mảnh lưu ly thủ công.",
        "care_instructions": "Chỉ giặt khô. Không ngâm nước. Bảo quản đứng hoặc cuộn nhẹ trong giấy acid-free.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Trầm Lam – Tradition",
        "slug": "tram-lam-tradition",
        "price": 10_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Tradition",
        "is_new": False,
        "is_featured": False,
        "sort_order": 7,
        "color_hex": "#3a5a7a",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Bảng màu này được dẫn dắt bởi sắc Trầm Lam, một gam xanh xám pha ảnh khói, sâu và tĩnh. "
            "Màu sắc mang cảm giác chín muồi, không lạnh, không sáng gắt gợi chiều sâu nội tại và "
            "sự điềm đạm của vẻ đẹp đã được tinh luyện qua thời gian với khí chất trang nhã.\n\n"
            "Trầm Lam là bảng màu của sự chín chắn và chiều sâu không phô trương, không xu hướng, "
            "mà sang trọng bằng sự điềm tĩnh và bền vững trong sắc độ."
        ),
        "fabric": "Lụa tơ tằm nhuộm thủ công màu Trầm Lam, kết hợp sợi bạc dệt xen tạo hiệu ứng ánh kim tinh tế.",
        "care_instructions": "Giặt tay hoặc giặt khô. Nước mát. Phơi trong bóng râm. Là ủi mặt trái với nhiệt độ thấp.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Thanh Lục Kim Hổ Phách – Peacock",
        "slug": "thanh-luc-kim-ho-phach",
        "price": 12_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Peacock",
        "is_new": False,
        "is_featured": False,
        "sort_order": 8,
        "color_hex": "#4a8060",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Thanh Lục Kim Hổ Phách gợi lên vẻ đẹp của đuôi chim công rực rỡ – sắc xanh lục pha "
            "vàng hổ phách tạo nên hiệu ứng thị giác lung linh, biến đổi theo góc nhìn và ánh sáng.\n\n"
            "Thuộc dòng Peacock – bộ sưu tập lấy cảm hứng từ những loài chim quý hiếm và kỳ diệu "
            "của thiên nhiên Đông Nam Á."
        ),
        "fabric": "Lụa jacquard dệt hoa văn chim công, pha sợi metallic vàng tạo hiệu ứng ánh kim.",
        "care_instructions": "Giặt khô. Không vắt. Bảo quản trong túi vải mềm.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "Thanh Lục Hoàng Kim – Lập Xuân",
        "slug": "thanh-luc-hoang-kim-lap-xuan",
        "price": 12_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Lập Xuân",
        "is_new": False,
        "is_featured": False,
        "sort_order": 9,
        "color_hex": "#5a8040",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Thanh Lục Hoàng Kim – màu xanh lá non tươi mát pha ánh vàng kim tinh tế, gợi hình ảnh "
            "mầm non đâm chồi trong tiết Lập Xuân. Sắc xanh tươi mới mang đến cảm giác sinh động "
            "và đầy hy vọng."
        ),
        "fabric": "Lụa Hà Đông dệt tay, nhuộm xanh từ lá chàm kết hợp kỹ thuật in vàng truyền thống.",
        "care_instructions": "Giặt tay nhẹ, nước mát. Không vắt mạnh. Phơi phẳng.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    # ── Featured / Iconic ─────────────────────────────────────────────────
    {
        "name": "Những Cánh Hoa Lấp Lánh",
        "slug": "nhung-canh-hoa-lap-lanh",
        "price": 18_600_000,
        "category_slug": "ao-dai-madame",
        "sub_category": "Specialty",
        "is_new": False,
        "is_featured": True,
        "sort_order": 0,
        "color_hex": "#d4af37",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "Những Cánh Hoa Lấp Lánh – tác phẩm đỉnh cao của nghệ thuật thêu truyền thống Việt Nam, "
            "được điểm xuyết bởi hàng nghìn cánh hoa thêu tay lấp lánh ánh kim.\n\n"
            "Đây là sản phẩm giới hạn, mỗi chiếc được ký tên và đánh số bởi nhà thiết kế HUY VO."
        ),
        "fabric": "Gấm lụa cao cấp, thêu kim tuyến và đính cườm thủ công. Mỗi áo mất 120 giờ thêu tay.",
        "care_instructions": "Chỉ giặt khô. Bảo quản trong hộp cứng chuyên dụng. Tránh ánh sáng mạnh.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày. Quốc tế 7–14 ngày. Đóng gói quà tặng cao cấp.",
    },
    {
        "name": "The Grey First Lady",
        "slug": "the-grey-first-lady",
        "price": 22_600_000,
        "category_slug": "ao-dai-firstlady",
        "sub_category": "Peacock",
        "is_new": False,
        "is_featured": True,
        "sort_order": 1,
        "color_hex": "#8a8a8a",
        "sizes": ["32","34","36","38","40","42"],
        "description": (
            "The Grey First Lady – áo dài dòng FirstLady với tông xám bạc quý phái, mang vẻ đẹp "
            "của người phụ nữ lãnh đạo, tự tin và thanh lịch.\n\n"
            "Phom dáng được nghiên cứu kỹ lưỡng để tôn dáng và tạo cảm giác thoải mái suốt ngày dài."
        ),
        "fabric": "Lụa Charmeuse pha sợi bạc, nhập khẩu từ Ý. Bề mặt mềm mại như nước.",
        "care_instructions": "Giặt khô hoặc giặt tay với nước lạnh. Phơi thẳng.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày. Quốc tế 7–14 ngày.",
    },
    {
        "name": "Blue Lagoon – Bà Ba Mademoiselle",
        "slug": "ba-ba-mademoiselle-blue-lagoon",
        "price": 14_600_000,
        "category_slug": "ao-ba-ba-mademoiselle",
        "sub_category": "Bà Ba Mademoiselle",
        "is_new": False,
        "is_featured": True,
        "sort_order": 2,
        "color_hex": "#4a90a4",
        "sizes": ["S","M","L","XL"],
        "description": (
            "Blue Lagoon – bộ bà ba Mademoiselle với sắc xanh lam gợi nhớ đầm phá nhiệt đới trong "
            "vắt, kết hợp đường cắt may hiện đại và tinh tế.\n\n"
            "Kiểu dáng vừa kế thừa nét duyên dáng của trang phục truyền thống Nam Bộ, vừa mang hơi "
            "thở đương đại phù hợp với phong cách sống năng động."
        ),
        "fabric": "Vải linen cotton tự nhiên 55/45, nhuộm indigo truyền thống. Thoáng mát, thân thiện với môi trường.",
        "care_instructions": "Giặt máy nhẹ ở 30°C hoặc giặt tay. Phơi trong bóng mát.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
    {
        "name": "The White – Bà Ba Gabriella",
        "slug": "the-white-gabriella-ba-ba",
        "price": 16_600_000,
        "category_slug": "ba-ba-gabriella",
        "sub_category": "Bà Ba Gabriella",
        "is_new": False,
        "is_featured": True,
        "sort_order": 3,
        "color_hex": "#e8e4dc",
        "sizes": ["S","M","L","XL"],
        "description": (
            "The White Gabriella – bộ bà ba trắng tinh khôi trong dòng Gabriella, biểu tượng cho "
            "sự thuần khiết và vẻ đẹp vĩnh cửu.\n\n"
            "Đường may thủ công hoàn hảo đến từng chi tiết nhỏ nhất, kết hợp với chất liệu cao cấp "
            "tạo nên một tác phẩm thời trang vượt thời gian."
        ),
        "fabric": "Vải muslin cotton Ai Cập 100% cao cấp, mềm mại, thoáng khí và không nhàu.",
        "care_instructions": "Giặt tay với nước mát. Dùng chất tẩy nhẹ màu trắng. Phơi phẳng.",
        "shipping_info": "Giao hàng nội địa 3–5 ngày. Quốc tế 7–14 ngày. Đổi trả trong vòng 14 ngày.",
    },
]

# ── Collections ───────────────────────────────────────────────────────────
COLLECTIONS = [
    {
        "title":        "Dáng Lụa Từ Hoa",
        "subtitle":     "Câu chuyện của Mây",
        "slug":         "dang-lua-tu-hoa-cau-chuyen-cua-may",
        "description":  "Bộ sưu tập lấy cảm hứng từ những đám mây nhẹ nhàng và dòng chảy của lụa Việt.",
        "gradient":     "linear-gradient(160deg,#2c2620 0%,#4a3828 60%,#3a2e22 100%)",
        "accent_color": "#d4af37",
        "is_tall":      True,
        "sort_order":   0,
    },
    {
        "title":        "Bridal",
        "subtitle":     "A Wedding Dress",
        "slug":         "a-wedding-dress",
        "description":  "Bộ sưu tập áo cưới HUY VO – vẻ đẹp thanh khiết và lộng lẫy cho ngày trọng đại.",
        "gradient":     "linear-gradient(135deg,#e8e0d0 0%,#d4c8b0 100%)",
        "accent_color": "#b8972a",
        "is_tall":      False,
        "sort_order":   1,
    },
    {
        "title":        "WomenSwear",
        "subtitle":     "Phong Cách Đương Đại",
        "slug":         "womenswear-collection",
        "description":  "Thời trang nữ hiện đại mang dấu ấn HUY VO.",
        "gradient":     "linear-gradient(135deg,#1a1a18 0%,#2c2620 100%)",
        "accent_color": "#c0395a",
        "is_tall":      False,
        "sort_order":   2,
    },
    {
        "title":        "Timeless Perfection",
        "subtitle":     "Collection",
        "slug":         "timeless-perfection",
        "description":  "Sự hoàn hảo vượt thời gian – bộ sưu tập kinh điển của HUY VO.",
        "gradient":     "linear-gradient(135deg,#3a2e22 0%,#2a2218 100%)",
        "accent_color": "#7b9eb5",
        "is_tall":      False,
        "sort_order":   3,
    },
]


# ── Seed runner ───────────────────────────────────────────────────────────
def run():
    if db.is_closed():
        db.connect()

    if User.select().where(User.email == "admin@huyvo.com").exists():
        print("[seed] Database already seeded – skipping.")
        return

    print("[seed] Seeding database …")

    with db.atomic():
        # 1. Categories (top-level) + SubCategories
        cat_by_slug: dict[str, Category] = {}
        sub_by_slug: dict[str, SubCategory] = {}
        for order, (slug, name, subs) in enumerate(TAXONOMY):
            cat, _ = Category.get_or_create(
                slug=slug, defaults={"name": name, "sort_order": order},
            )
            cat_by_slug[slug] = cat
            for sub_order, (sub_slug, sub_name) in enumerate(subs):
                sub, _ = SubCategory.get_or_create(
                    slug=sub_slug,
                    defaults={"category": cat, "name": sub_name, "sort_order": sub_order},
                )
                sub_by_slug[sub_slug] = sub
        print(f"[seed]   {len(cat_by_slug)} categories, {len(sub_by_slug)} subcategories ready.")

        # 2. Products + Images + Sizes
        if Product.select().count() > 0:
            print("[seed]   Products already present – skipping product rows.")
        else:
            for p in PRODUCTS:
                # Dữ liệu demo còn ghi danh mục con theo tên cũ → quy về danh mục
                # cha trong cây hiện tại, danh mục con để admin chọn lại.
                old_slug = p["category_slug"]
                sub      = sub_by_slug.get(old_slug)
                category = sub.category if sub else cat_by_slug[
                    LEGACY_PRODUCT_CATEGORY.get(old_slug, TAXONOMY[0][0])
                ]
                product = Product.create(
                    name=p["name"],
                    slug=p["slug"],
                    price=Decimal(str(p["price"])),
                    description=p.get("description"),
                    fabric=p.get("fabric"),
                    care_instructions=p.get("care_instructions"),
                    shipping_info=p.get("shipping_info"),
                    category=category,
                    subcategory=sub,
                    primary_color=p.get("color_hex"),
                    is_new=p.get("is_new", False),
                    is_featured=p.get("is_featured", False),
                    sort_order=p.get("sort_order", 0),
                )
                from app.storage import save_placeholder
                placeholder_url = save_placeholder(product.slug, product.name, p.get("color_hex"))
                ProductImage.create(
                    product=product,
                    url=placeholder_url,
                    alt_text=product.name,
                    sort_order=0,
                    is_primary=True,
                )
                for sz in p.get("sizes", []):
                    ProductSize.create(product=product, size=sz, stock=5, is_available=True)

            print(f"[seed]   {len(PRODUCTS)} products created.")

        # 3. Collections
        if Collection.select().count() == 0:
            for c in COLLECTIONS:
                Collection.create(
                    name=c["title"],
                    slug=c["slug"],
                    subtitle=c.get("subtitle"),
                    description=c.get("description"),
                    gradient=c.get("gradient"),
                    accent_color=c.get("accent_color"),
                    sort_order=c.get("sort_order", 0),
                )
            print(f"[seed]   {len(COLLECTIONS)} collections created.")
        else:
            print("[seed]   Collections already present – skipping.")

        # 4. Admin user
        User.get_or_create(
            email="admin@huyvo.com",
            defaults={
                "full_name": "HUY VO Admin",
                "hashed_password": hash_password("Admin@123"),
                "is_admin": True,
            },
        )
        print("[seed]   Admin user: admin@huyvo.com / Admin@123")

    print("[seed] Done ✓")


if __name__ == "__main__":
    run()
