import { ref } from 'vue'
import { productsApi, categoriesApi } from '@/api'

/**
 * Sản phẩm vải thật (tạo từ trang admin) cho 2 trang kho lụa.
 * Các mẫu trong `@/data/fabrics` là dữ liệu demo tĩnh; composable này bổ sung
 * hàng thật vào lưới, link sang /san-pham/{slug}.
 *
 * Tách theo danh mục con: 'lua-nha-xa-100-to-tam' → trang 100% tơ tằm,
 * còn lại (kể cả sản phẩm chưa chọn danh mục con) → trang thông dụng.
 */
const FABRIC_CATEGORY_SLUG = 'lua-to-tam'
const PURE_SILK_SUB_SLUG   = 'lua-nha-xa-100-to-tam'

export function useFabricProducts() {
  const common   = ref([])
  const pureSilk = ref([])
  const loading  = ref(false)

  async function fetch() {
    loading.value = true
    try {
      const [cats, data] = await Promise.all([
        categoriesApi.list(),
        productsApi.list({ category: FABRIC_CATEGORY_SLUG, per_page: 100 }),
      ])
      // API sản phẩm trả về tên danh mục con (sub_category), không trả slug →
      // tra tên tương ứng với slug từ cây danh mục.
      const cat      = (Array.isArray(cats) ? cats : []).find(c => c.slug === FABRIC_CATEGORY_SLUG)
      const pureName = cat?.subcategories?.find(s => s.slug === PURE_SILK_SUB_SLUG)?.name
      const items    = data.results ?? []

      pureSilk.value = pureName ? items.filter(p => p.sub_category === pureName) : []
      common.value   = pureName ? items.filter(p => p.sub_category !== pureName) : items
    } catch (e) {
      common.value   = []
      pureSilk.value = []
      console.error('[useFabricProducts]', e)
    } finally {
      loading.value = false
    }
  }

  fetch()
  return { common, pureSilk, loading, fetch }
}

/** Ảnh đại diện thật của sản phẩm (bỏ qua ảnh placeholder tự sinh). */
export function productImage(p) {
  const url = p?.images?.[0]?.url
  return url && !url.includes('/placeholder/') ? url : null
}

/** Nền cho card khi sản phẩm chưa có ảnh thật. */
export function productGradient(p) {
  const hex = p?.images?.[0]?.color_hex
  if (!hex) return 'linear-gradient(145deg, #ece5d5 0%, #d4c8b0 100%)'
  return `linear-gradient(145deg, ${hex} 0%, ${hex}CC 60%, ${hex}99 100%)`
}
