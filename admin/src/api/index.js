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
  list:   (params) => client.get('/products/', { params }),
  get:    (slug)   => client.get(`/products/${slug}`),
  create: (data)   => client.post('/products/', data),
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

// ── Uploads (ảnh chèn trong nội dung, video nền trang chủ) ────────────────
export const uploadsApi = {
  image: (formData) => client.post('/uploads/image', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  video: (formData, onProgress) => client.post('/uploads/video', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 0,                       // video lớn, không giới hạn thời gian
    onUploadProgress: onProgress,
  }),
}

// ── Cấu hình nội dung website ─────────────────────────────────────────────
export const settingsApi = {
  list: ()            => client.get('/settings/'),
  save: (key, value)  => client.put(`/settings/${key}`, { value }),
}

// ── Bài viết (Tin tức) ────────────────────────────────────────────────────
export const postsApi = {
  list:   (params) => client.get('/posts/', { params: { published_only: false, ...params } }),
  get:    (idOrSlug) => client.get(`/posts/${idOrSlug}`),
  create: (data)   => client.post('/posts/', data),
  update: (id, data) => client.put(`/posts/${id}`, data),
  remove: (id)     => client.delete(`/posts/${id}`),
}

// ── Categories ────────────────────────────────────────────────────────────
export const categoriesApi = {
  list:   ()       => client.get('/categories/', { params: { active_only: false } }),
  create: (data)   => client.post('/categories/', data),
  update: (id, data) => client.put(`/categories/${id}`, data),
  remove: (id)     => client.delete(`/categories/${id}`),

  // Subcategories
  createSub: (catId, data) => client.post(`/categories/${catId}/subcategories`, data),
  updateSub: (id, data)    => client.put(`/subcategories/${id}`, data),
  deleteSub: (id)          => client.delete(`/subcategories/${id}`),
}

// ── Orders ────────────────────────────────────────────────────────────────
export const ordersApi = {
  list:         (params) => client.get('/orders/', { params }),
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
  listGrouped: ()          => client.get('/customization-options/'),
  listAll:     ()          => client.get('/customization-options/all'),
  create:      (data)      => client.post('/customization-options/', data),
  update:      (id, data)  => client.put(`/customization-options/${id}`, data),
  remove:      (id)        => client.delete(`/customization-options/${id}`),
}

// ── Newsletter ────────────────────────────────────────────────────────────
export const newsletterApi = {
  subscribers: (params) => client.get('/newsletter/subscribers', { params }),
}
