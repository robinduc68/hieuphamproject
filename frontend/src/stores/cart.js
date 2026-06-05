import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // Persist cart in localStorage
  const _load = () => {
    try { return JSON.parse(localStorage.getItem('huyvo_cart') || '[]') } catch { return [] }
  }

  const items = ref(_load())

  const count = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))
  const total = computed(() =>
    items.value.reduce((s, i) => s + i.price * i.quantity, 0)
  )

  function _save() {
    localStorage.setItem('huyvo_cart', JSON.stringify(items.value))
  }

  function addItem(product, size, quantity = 1) {
    const idx = items.value.findIndex(
      (i) => i.product_id === product.id && i.size === size
    )
    if (idx !== -1) {
      items.value[idx].quantity += quantity
    } else {
      items.value.push({
        product_id: product.id,
        slug:       product.slug,
        name:       product.name,
        price:      Number(product.price),
        color_hex:  product.images?.[0]?.color_hex ?? null,
        size,
        quantity,
      })
    }
    _save()
  }

  function removeItem(productId, size) {
    items.value = items.value.filter(
      (i) => !(i.product_id === productId && i.size === size)
    )
    _save()
  }

  function updateQty(productId, size, quantity) {
    const item = items.value.find(
      (i) => i.product_id === productId && i.size === size
    )
    if (item) {
      if (quantity <= 0) removeItem(productId, size)
      else item.quantity = quantity
    }
    _save()
  }

  function clear() {
    items.value = []
    _save()
  }

  /** Build payload for POST /api/orders/ */
  function toOrderItems() {
    return items.value.map((i) => ({
      product_id: i.product_id,
      size:       i.size,
      quantity:   i.quantity,
    }))
  }

  return { items, count, total, addItem, removeItem, updateQty, clear, toOrderItems }
})
