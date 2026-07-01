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

export function fabricGradient(c1, c2) {
  return `linear-gradient(145deg, ${c1} 0%, ${c2} 60%, ${c1}CC 100%)`
}

export function getFabric(id) {
  return fabrics.find(f => String(f.id) === String(id)) || null
}
