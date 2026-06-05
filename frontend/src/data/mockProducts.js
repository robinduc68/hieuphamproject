export const mockProduct = {
  id: 1,
  slug: 'hong-sakura-lap-xuan',
  name: 'Hồng Sakura – Lập Xuân',
  price: 12600000,
  price_min: 10600000,
  is_new: true,
  description: `Sắc hồng đào pha ánh vàng — tựa như những cánh sakura đầu tiên của mùa xuân chạm nhẹ lên mặt lụa, mang theo hơi thở thanh thoát và thuần khiết của đất trời giao mùa.\n\nHiệu ứng lấp lánh tinh tế được tạo ra bởi kỹ thuật dệt độc quyền, kết hợp sợi tơ tằm tự nhiên với chỉ ánh bạc — phản chiếu ánh sáng một cách dịu dàng, không chói, tôn lên nét duyên dáng của người mặc trong từng chuyển động.`,
  category: {
    name: 'MODERN HERITAGE',
    slug: 'modern-heritage',
  },
  sub_category: 'Áo Dài Madame',
  images: [
    { color_hex: '#E8A0A8' },
    { color_hex: '#D4788A' },
    { color_hex: '#C05870' },
    { color_hex: '#A84060' },
  ],
  sizes: [
    { id: 1, size: '32', in_stock: true },
    { id: 2, size: '34', in_stock: true },
    { id: 3, size: '36', in_stock: true },
    { id: 4, size: '38', in_stock: false },
    { id: 5, size: '40', in_stock: true },
    { id: 6, size: '42', in_stock: true },
  ],
  fabric:
    'Lụa tơ tằm cao cấp được dệt thủ công tại Hội An, kết hợp kỹ thuật thêu tay truyền thống của nghệ nhân Việt Nam. Chất liệu thoáng mát, mềm mại, giữ form suốt cả ngày dài.',
  care_instructions:
    'Giặt khô (dry clean only). Không giặt máy, không vắt xoắn. Bảo quản nơi khô thoáng, treo thẳng, tránh ánh nắng trực tiếp và nhiệt độ cao.',
  shipping_info:
    'Giao hàng nội địa 3–5 ngày làm việc. Quốc tế 7–14 ngày. Miễn phí đổi trả trong 7 ngày với sản phẩm chưa qua sử dụng và còn nguyên tag.',
}

export const mockRelated = [
  {
    id: 2,
    slug: 'vang-kim-hoang-lap-xuan',
    name: 'Vàng Kim Hoàng – Lập Xuân',
    price: '10.600.000 đ',
    color: '#D4A853',
    isNew: false,
    sizes: ['32', '34', '36', '38', '40'],
  },
  {
    id: 3,
    slug: 'the-dong-dong-lap-xuan',
    name: 'The Đồng Đồng – Lập Xuân',
    price: '12.600.000 đ',
    color: '#B87A5A',
    isNew: true,
    sizes: ['34', '36', '38', '40', '42'],
  },
  {
    id: 4,
    slug: 'thanh-luc-hoang-kim-lap-xuan',
    name: 'Thanh Lục Hoàng Kim – Lập Xuân',
    price: '12.600.000 đ',
    color: '#7A9E6A',
    isNew: false,
    sizes: ['32', '34', '36', '38'],
  },
  {
    id: 5,
    slug: 'sac-xam-luc-bao',
    name: 'Sắc Xám Lục Bảo',
    price: '10.600.000 đ',
    color: '#6A8E8A',
    isNew: false,
    sizes: ['34', '36', '38', '40', '42'],
  },
]
