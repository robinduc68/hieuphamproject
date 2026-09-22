import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const _load = () => {
    try { return JSON.parse(localStorage.getItem('huyvo_cart') || '[]') } catch { return [] }
  }

  const items = ref(_load())

  /** Làm tròn 1 chữ số lẻ — tránh 0.1 + 0.2 = 0.30000000000000004 */
  const round1 = (v) => Math.round(Number(v) * 10) / 10

  // Đếm theo SỐ DÒNG chứ không cộng số lượng: vải mua 3.8 mét thì badge hiện
  // "3.8" rất vô nghĩa.
  const count = computed(() => items.value.length)
  const total = computed(() =>
    items.value.reduce((s, i) => s + i.price * i.quantity, 0)
  )

  function _save() {
    localStorage.setItem('huyvo_cart', JSON.stringify(items.value))
  }

  /**
   * @param {object} product
   * @param {string} size
   * @param {number} quantity
   * @param {{ tailoring_method, lining_type, color_option, price_adjustment }} customization
   */
  function addItem(product, size, quantity = 1, customization = {}) {
    quantity = round1(quantity)
    const unitPrice = Number(product.price) + Number(customization.price_adjustment ?? 0)
    // Unique key includes all selections so different combos are separate cart lines
    const key = [
      product.id,
      size,
      customization.tailoring_method ?? '',
      customization.lining_type ?? '',
      customization.color_option ?? '',
    ].join('|')

    const idx = items.value.findIndex(i => i._key === key)
    if (idx !== -1) {
      items.value[idx].quantity = round1(items.value[idx].quantity + quantity)
    } else {
      items.value.push({
        _key:             key,
        product_id:       product.id,
        slug:             product.slug,
        name:             product.name,
        price:            unitPrice,
        color_hex:        product.images?.[0]?.color_hex ?? null,
        size,
        quantity,
        // Vải bán theo mét (số lẻ) → giỏ hàng và thanh toán hiển thị khác quần áo
        product_type: product.product_type ?? 'apparel',
        unit_label:   product.unit_label?.trim() || 'mét',
        tailoring_method: customization.tailoring_method ?? null,
        lining_type:      customization.lining_type ?? null,
        color_option:     customization.color_option ?? null,
      })
    }
    _save()
  }

  function removeItem(key) {
    items.value = items.value.filter(i => i._key !== key)
    _save()
  }

  function updateQty(key, quantity) {
    const item = items.value.find(i => i._key === key)
    if (item) {
      const qty = round1(quantity)
      if (qty <= 0) removeItem(key)
      else item.quantity = qty
    }
    _save()
  }

  function clear() {
    items.value = []
    _save()
  }

  function toOrderItems() {
    return items.value.map(i => ({
      product_id:       i.product_id,
      size:             i.size,
      quantity:         i.quantity,
      tailoring_method: i.tailoring_method,
      lining_type:      i.lining_type,
      color_option:     i.color_option,
    }))
  }

  return { items, count, total, addItem, removeItem, updateQty, clear, toOrderItems }
})
