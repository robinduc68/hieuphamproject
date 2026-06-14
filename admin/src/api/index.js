import client from './client.js'

// ── Auth ──────────────────────────────────────────────────────────────────
export const authApi = {
  login:  (data) => client.post('/users/login', data),
  me:     ()     => client.get('/users/me'),
}

// ── Stats ─────────────────────────────────────────────────────────────────
export const statsApi = {
  get: () => client.get('/admin/stats'),
}

// ── Products ──────────────────────────────────────────────────────────────
export const productsApi = {
  list:   (params) => client.get('/products', { params }),
  get:    (slug)   => client.get(`/products/${slug}`),
  create: (data)   => client.post('/products', data),
  update: (id, data) => client.put(`/products/${id}`, data),
  remove: (id)     => client.delete(`/products/${id}`),

  // Images
  uploadImage:  (id, formData) => client.post(`/products/${id}/images`, formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  updateImage:  (id, imgId, data) => client.put(`/products/${id}/images/${imgId}`, data),
  deleteImage:  (id, imgId)   => client.delete(`/products/${id}/images/${imgId}`),
  reorderImages:(id, data)    => client.patch(`/products/${id}/images/reorder`, data),

  // Sizes
  addSize:    (id, data)       => client.post(`/products/${id}/sizes`, data),
  updateSize: (id, sizeId, data) => client.put(`/products/${id}/sizes/${sizeId}`, data),
  deleteSize: (id, sizeId)    => client.delete(`/products/${id}/sizes/${sizeId}`),
}

// ── Categories ────────────────────────────────────────────────────────────
export const categoriesApi = {
  list:   ()       => client.get('/categories', { params: { active_only: false } }),
  create: (data)   => client.post('/categories', data),
  update: (id, data) => client.put(`/categories/${id}`, data),
  remove: (id)     => client.delete(`/categories/${id}`),

  // Subcategories
  createSub: (catId, data) => client.post(`/categories/${catId}/subcategories`, data),
  updateSub: (id, data)    => client.put(`/subcategories/${id}`, data),
  deleteSub: (id)          => client.delete(`/subcategories/${id}`),
}

// ── Orders ────────────────────────────────────────────────────────────────
export const ordersApi = {
  list:         (params) => client.get('/orders', { params }),
  get:          (id)     => client.get(`/orders/${id}`),
  updateStatus: (id, data) => client.patch(`/orders/${id}/status`, data),
}

// ── Users ─────────────────────────────────────────────────────────────────
export const usersApi = {
  list:   (params)     => client.get('/admin/users', { params }),
  update: (id, data)   => client.put(`/admin/users/${id}`, data),
  remove: (id)         => client.delete(`/admin/users/${id}`),
}

// ── Customization options ─────────────────────────────────────────────────
export const customizationApi = {
  listGrouped: ()          => client.get('/customization-options'),
  listAll:     ()          => client.get('/customization-options/all'),
  create:      (data)      => client.post('/customization-options', data),
  update:      (id, data)  => client.put(`/customization-options/${id}`, data),
  remove:      (id)        => client.delete(`/customization-options/${id}`),
}

// ── Newsletter ────────────────────────────────────────────────────────────
export const newsletterApi = {
  subscribers: (params) => client.get('/newsletter/subscribers', { params }),
}
