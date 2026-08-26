import { ref } from 'vue'
import { categoriesApi } from '@/api'

/**
 * Cây danh mục lấy từ API, cache ở tầng module để header + trang shop
 * dùng chung một lần fetch.
 */
const categories = ref([])
const loading    = ref(false)
const error      = ref(null)
let inflight     = null

/** Danh mục có trang riêng thay vì lọc trong /cua-hang */
export const DIRECT_ROUTES = { 'lua-to-tam': '/lua-to-tam' }

function load(force = false) {
  if (inflight && !force) return inflight
  loading.value = true
  error.value   = null
  inflight = categoriesApi
    .list()
    .then((data) => {
      categories.value = Array.isArray(data) ? data : (data?.results ?? [])
      return categories.value
    })
    .catch((e) => {
      error.value = 'Không tải được danh mục.'
      console.error('[useCategories]', e)
      categories.value = []
      inflight = null      // cho phép thử lại ở lần gọi sau
      return []
    })
    .finally(() => { loading.value = false })
  return inflight
}

export function useCategories() {
  load()
  return { categories, loading, error, reload: () => load(true) }
}

/**
 * Tìm slug thuộc danh mục cha hay danh mục con.
 * → { type: 'category' | 'subcategory' | null, category, subcategory }
 */
export function resolveSlug(slug, list = categories.value) {
  if (!slug) return { type: null, category: null, subcategory: null }
  for (const cat of list) {
    if (cat.slug === slug) return { type: 'category', category: cat, subcategory: null }
    for (const sub of cat.subcategories ?? []) {
      if (sub.slug === slug) return { type: 'subcategory', category: cat, subcategory: sub }
    }
  }
  return { type: null, category: null, subcategory: null }
}
