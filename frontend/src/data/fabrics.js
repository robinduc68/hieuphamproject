// Shared fabric catalog — used by FabricView (listing) and FabricDetailView (SP vải).
// ponytail: static local data; move to API only if the catalog needs a backend.

export const fabrics = [
  { id:  1, code: 'TD01', name: 'THỌ DƠI - HỒNG ÁNH VÀNG',   color1: '#E8B4BC', color2: '#D4A0A8', pattern: 'Thọ Dơi',      colorTag: 'Hồng',    price: 162000 },
  { id:  2, code: 'TD02', name: 'THỌ DƠI - HỒNG ÁNH VÀNG 02', color1: '#DDA8B0', color2: '#C89098', pattern: 'Thọ Dơi',      colorTag: 'Hồng',    price: 162000 },
  { id:  3, code: 'TD03', name: 'CÚC - HỒNG ÁNH VÀNG',        color1: '#F0C0C8', color2: '#E0A8B0', pattern: 'Cúc',          colorTag: 'Hồng',    price: 162000 },
  { id:  4, code: 'DC04', name: 'ĐUÔI CÔNG - HỒNG ÁNH VÀNG',  color1: '#E4B0B8', color2: '#D49098', pattern: 'Đuôi Công',    colorTag: 'Hồng',    price: 168000 },
  { id:  5, code: 'CD05', name: 'CÚC ĐẠI ĐÓA - VÀNG CỔ ĐIỂN', color1: '#D4B060', color2: '#C09840', pattern: 'Cúc Đại Đóa',  colorTag: 'Vàng',    price: 175000 },
  { id:  6, code: 'HM06', name: 'HOA MAI - VÀNG',             color1: '#DEC070', color2: '#CAA850', pattern: 'Hoa Mai',      colorTag: 'Vàng',    price: 168000 },
  { id:  7, code: 'PT07', name: 'PHÚC THỌ - ĐỎ',              color1: '#C04050', color2: '#A02838', pattern: 'Phúc Thọ',     colorTag: 'Đỏ',      price: 180000 },
  { id:  8, code: 'LP08', name: 'LONG PHỤNG - ĐỎ',            color1: '#D05060', color2: '#B03848', pattern: 'Long Phụng',   colorTag: 'Đỏ',      price: 195000 },
  { id:  9, code: 'ST09', name: 'SEN TRÒN - XANH LÁ',         color1: '#4A8860', color2: '#367048', pattern: 'Sen Tròn',     colorTag: 'Xanh lá', price: 168000 },
  { id: 10, code: 'TT10', name: 'THỦY TIÊN - TÍM',            color1: '#9070B8', color2: '#7858A0', pattern: 'Thủy Tiên',    colorTag: 'Tím',     price: 172000 },
  { id: 11, code: 'TM11', name: 'TRÚC MAI - BE',              color1: '#D8C8A8', color2: '#C8B890', pattern: 'Trúc Mai',     colorTag: 'Be',      price: 162000 },
  { id: 12, code: 'CH12', name: 'CÚC HOA - ĐEN',              color1: '#404040', color2: '#282828', pattern: 'Cúc',          colorTag: 'Đen',     price: 168000 },
  { id: 13, code: 'SH13', name: 'SEN HỔ ĐIỆP - HỒNG',         color1: '#F0A8B8', color2: '#E09098', pattern: 'Sen - Hổ Điệp', colorTag: 'Hồng',   price: 175000 },
  { id: 14, code: 'LP14', name: 'ĐÔI LONG - VÀNG',            color1: '#E8C878', color2: '#D4B060', pattern: 'Long Phụng',   colorTag: 'Vàng',    price: 195000 },
  { id: 15, code: 'SH15', name: 'HỔ ĐIỆP - CAM',              color1: '#E89060', color2: '#D07848', pattern: 'Sen - Hổ Điệp', colorTag: 'Cam',    price: 175000 },
  { id: 16, code: 'DC16', name: 'ĐÔI PHỤNG - NÂU',            color1: '#A07858', color2: '#886040', pattern: 'Đuôi Công',    colorTag: 'Nâu',     price: 180000 },
]

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

export const pureSilkFabrics = [
  { id: 101, code: 'LM01', name: 'LOANG MÀU - HỒNG ĐÀO',   color1: '#F0B8C0', color2: '#C98A98', silkType: 'Lụa Loang màu 100% tơ tằm', pattern: 'Loang màu', colorTag: 'Hồng',    price: 285000 },
  { id: 102, code: 'LM02', name: 'LOANG MÀU - XANH NGỌC',  color1: '#7FC4B8', color2: '#3F8F84', silkType: 'Lụa Loang màu 100% tơ tằm', pattern: 'Loang màu', colorTag: 'Xanh lá', price: 285000 },
  { id: 103, code: 'LM03', name: 'LOANG MÀU - TÍM KHÓI',   color1: '#A98CC0', color2: '#7A5F96', silkType: 'Lụa Loang màu 100% tơ tằm', pattern: 'Loang màu', colorTag: 'Tím',     price: 285000 },
  { id: 104, code: 'LM04', name: 'LOANG MÀU - CAM SAN HÔ', color1: '#F0A070', color2: '#D07040', silkType: 'Lụa Loang màu 100% tơ tằm', pattern: 'Loang màu', colorTag: 'Cam',     price: 290000 },

  { id: 111, code: 'LT01', name: 'TRƠN - TRẮNG NGÀ',       color1: '#F7F3EA', color2: '#E6DFD0', silkType: 'Lụa Trơn 100% tơ tằm',      pattern: 'Trơn',      colorTag: 'Trắng',   price: 265000 },
  { id: 112, code: 'LT02', name: 'TRƠN - ĐỎ ĐÔ',           color1: '#C0374A', color2: '#8E2333', silkType: 'Lụa Trơn 100% tơ tằm',      pattern: 'Trơn',      colorTag: 'Đỏ',      price: 268000 },
  { id: 113, code: 'LT03', name: 'TRƠN - VÀNG HOÀNG YẾN',  color1: '#E8CA72', color2: '#CFAC4C', silkType: 'Lụa Trơn 100% tơ tằm',      pattern: 'Trơn',      colorTag: 'Vàng',    price: 265000 },
  { id: 114, code: 'LT04', name: 'TRƠN - XANH LAM ĐÊM',    color1: '#3B4A8C', color2: '#232F63', silkType: 'Lụa Trơn 100% tơ tằm',      pattern: 'Trơn',      colorTag: 'Xanh lam',price: 268000 },
  { id: 115, code: 'LT05', name: 'TRƠN - ĐEN HUYỀN',       color1: '#3A3A3A', color2: '#1E1E1E', silkType: 'Lụa Trơn 100% tơ tằm',      pattern: 'Trơn',      colorTag: 'Đen',     price: 268000 },

  { id: 121, code: 'LH01', name: 'HỌA TIẾT - LONG PHỤNG ĐỎ',   color1: '#CE4C5C', color2: '#A02E3E', silkType: 'Lụa họa tiết 100% tơ tằm', pattern: 'Long Phụng',  colorTag: 'Đỏ',    price: 320000 },
  { id: 122, code: 'LH02', name: 'HỌA TIẾT - CÚC ĐẠI ĐÓA VÀNG', color1: '#DCB962', color2: '#BE9840', silkType: 'Lụa họa tiết 100% tơ tằm', pattern: 'Cúc Đại Đóa', colorTag: 'Vàng',  price: 315000 },
  { id: 123, code: 'LH03', name: 'HỌA TIẾT - SEN TRÒN XANH',    color1: '#4F926A', color2: '#357350', silkType: 'Lụa họa tiết 100% tơ tằm', pattern: 'Sen Tròn',    colorTag: 'Xanh lá', price: 315000 },
  { id: 124, code: 'LH04', name: 'HỌA TIẾT - THỌ DƠI HỒNG',     color1: '#EBB0BA', color2: '#CE8C99', silkType: 'Lụa họa tiết 100% tơ tằm', pattern: 'Thọ Dơi',     colorTag: 'Hồng',  price: 315000 },
]

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
