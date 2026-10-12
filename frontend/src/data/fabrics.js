// Dữ liệu dùng chung cho 2 trang kho lụa (FabricView, PureSilkView) và trang
// chi tiết mẫu vải.
//
// `fabrics` / `pureSilkFabrics` trước đây chứa mẫu demo (ô màu gradient) để
// dựng giao diện khi chưa có hàng thật. Đã xoá — hai trang giờ chỉ hiển thị
// sản phẩm vải tạo từ trang admin.
//
// Phần còn lại vẫn dùng: `patterns` (danh sách họa tiết dự phòng khi admin
// chưa cấu hình ở Nội dung web), `colors` và `silkTypes` cho sidebar lọc.

export const fabrics = []

export const patterns = [
  'Thọ Dơi', 'Đuôi Công', 'Cúc', 'Cúc Đại Đóa',
  'Sen Tròn', 'Sen - Hổ Điệp', 'Thủy Tiên', 'Phúc Thọ',
  'Long Phụng', 'Hoa Mai', 'Hoa Đào', 'Trúc Mai',
]

export const colors = [
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

/* ── Lụa Nha Xá 100% tơ tằm ─────────────────────────────
   Bộ lọc theo loại lụa (không lọc theo họa tiết như trang thông dụng). */
export const silkTypes = [
  'Lụa Loang màu 100% tơ tằm',
  'Lụa Trơn 100% tơ tằm',
  'Lụa họa tiết 100% tơ tằm',
]

export const pureSilkFabrics = []

export function fabricGradient(c1, c2) {
  return `linear-gradient(145deg, ${c1} 0%, ${c2} 60%, ${c1}CC 100%)`
}

/** Tất cả mẫu vải của cả 2 trang — dùng cho trang chi tiết. */
export const allFabrics = [...fabrics, ...pureSilkFabrics]

export function getFabric(id) {
  return allFabrics.find(f => String(f.id) === String(id)) || null
}

/** Bộ sưu tập chứa mẫu vải này (thông dụng hay 100% tơ tằm). */
export function collectionOf(id) {
  return pureSilkFabrics.some(f => String(f.id) === String(id)) ? pureSilkFabrics : fabrics
}
