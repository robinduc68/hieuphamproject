// Tuỳ chọn bộ lọc của 2 trang kho lụa ngoài website.
// Phải khớp với frontend/src/data/fabrics.js — tên ở đây được lưu thẳng vào
// products.pattern / color_tag / silk_type và đem so sánh với bộ lọc bên đó.

export const PATTERNS = [
  'Thọ Dơi', 'Đuôi Công', 'Cúc', 'Cúc Đại Đóa',
  'Sen Tròn', 'Sen - Hổ Điệp', 'Thủy Tiên', 'Phúc Thọ',
  'Long Phụng', 'Hoa Mai', 'Hoa Đào', 'Trúc Mai',
]

export const COLOR_TAGS = [
  { name: 'Đỏ',       hex: '#E53935' },
  { name: 'Vàng',     hex: '#FDD835' },
  { name: 'Hồng',     hex: '#F06292' },
  { name: 'Be',       hex: '#EDE0C8' },
  { name: 'Cam',      hex: '#FB8C00' },
  { name: 'Xanh lá',  hex: '#2E7D32' },
  { name: 'Xanh lam', hex: '#1A237E' },
  { name: 'Tím',      hex: '#9575CD' },
  { name: 'Nâu',      hex: '#6D4C41' },
  { name: 'Trắng',    hex: '#FFFFFF' },
  { name: 'Đen',      hex: '#212121' },
  { name: 'Xám',      hex: '#9E9E9E' },
]

export const SILK_TYPES = [
  'Lụa Loang màu 100% tơ tằm',
  'Lụa Trơn 100% tơ tằm',
  'Lụa họa tiết 100% tơ tằm',
]
