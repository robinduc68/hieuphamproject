import { ref, watch } from 'vue'
import { productsApi } from '@/api'

/** Thông báo lỗi đọc được thay vì [object Object] */
function apiError(e, fallback) {
  return e?.response?.data?.detail || e?.message || fallback
}

/** Paginated product list with filters */
export function useProducts(initialParams = {}) {
  const products  = ref([])
  const total     = ref(0)
  const loading   = ref(false)
  const error     = ref(null)
  const params    = ref({ page: 1, per_page: 12, ...initialParams })

  async function fetch() {
    loading.value = true
    error.value   = null
    try {
      const data      = await productsApi.list(params.value)
      products.value  = data.results ?? []
      total.value     = data.total ?? 0
    } catch (e) {
      products.value = []
      total.value    = 0
      error.value    = apiError(e, 'Không tải được danh sách sản phẩm.')
      console.error('[useProducts]', e)
    } finally {
      loading.value = false
    }
  }

  watch(params, fetch, { deep: true, immediate: true })

  return { products, total, loading, error, params, fetch }
}

/** Single product detail */
export function useProduct(slug) {
  const product = ref(null)
  const loading = ref(false)
  const error   = ref(null)

  async function fetch() {
    if (!slug.value && !slug) return
    loading.value = true
    error.value   = null
    try {
      product.value = await productsApi.detail(
        typeof slug === 'string' ? slug : slug.value
      )
    } catch (e) {
      product.value = null
      error.value   = apiError(e, 'Không tìm thấy sản phẩm.')
      console.error('[useProduct]', e)
    } finally {
      loading.value = false
    }
  }

  if (typeof slug === 'string') {
    fetch()
  } else {
    watch(slug, fetch, { immediate: true })
  }

  return { product, loading, error, fetch }
}

/** New arrivals */
export function useNewArrivals(limit = 10) {
  const products = ref([])
  const loading  = ref(false)
  const error    = ref(null)

  async function fetch() {
    loading.value = true
    try {
      products.value = await productsApi.newArrivals(limit)
    } catch (e) {
      products.value = []
      error.value    = apiError(e, 'Không tải được sản phẩm mới.')
      console.error('[useNewArrivals]', e)
    } finally {
      loading.value = false
    }
  }

  fetch()
  return { products, loading, error, fetch }
}

/** Featured products */
export function useFeaturedProducts(limit = 4) {
  const products = ref([])
  const loading  = ref(false)

  async function fetch() {
    loading.value = true
    try {
      products.value = await productsApi.featured(limit)
    } catch (e) {
      products.value = []
      console.error('[useFeaturedProducts]', e)
    } finally {
      loading.value = false
    }
  }

  fetch()
  return { products, loading, fetch }
}
