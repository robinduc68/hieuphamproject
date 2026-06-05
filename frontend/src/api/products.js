import client from './client'

export const productsApi = {
  /** Danh sách sản phẩm có phân trang & filter */
  list(params = {}) {
    return client.get('/products/', { params }).then((r) => r.data)
  },

  /** Sản phẩm mới nhất */
  newArrivals(limit = 10) {
    return client.get('/products/new-arrivals', { params: { limit } }).then((r) => r.data)
  },

  /** Sản phẩm nổi bật */
  featured(limit = 4) {
    return client.get('/products/featured', { params: { limit } }).then((r) => r.data)
  },

  /** Chi tiết 1 sản phẩm theo slug */
  detail(slug) {
    return client.get(`/products/${slug}`).then((r) => r.data)
  },

  /** Danh mục sản phẩm */
  categories() {
    return client.get('/categories/').then((r) => r.data)
  },

  /** Upload ảnh (admin) */
  uploadImage(productId, file, colorHex) {
    const form = new FormData()
    form.append('file', file)
    if (colorHex) form.append('color_hex', colorHex)
    return client
      .post(`/products/${productId}/images`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then((r) => r.data)
  },
}

export const categoriesApi = {
  list() {
    return client.get('/categories/').then((r) => r.data)
  },
  detail(slug) {
    return client.get(`/categories/${slug}`).then((r) => r.data)
  },
}
