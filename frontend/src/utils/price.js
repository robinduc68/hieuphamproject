/** Giá tiền Việt: 18600000 -> "18.600.000 đ". Trả '' nếu không phải số. */
export function formatPrice(value) {
  const n = Number(value)
  if (!Number.isFinite(n)) return ''
  return n.toLocaleString('vi-VN') + ' đ'
}

/**
 * Giá hiện trên card sản phẩm. API trả price dạng chuỗi ("18600000") nên chỗ
 * nào in thẳng sẽ ra số không định dạng — luôn đi qua hàm này.
 */
export function productPriceLabel(product) {
  return formatPrice(product?.price)
}
