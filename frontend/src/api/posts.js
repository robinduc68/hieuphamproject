import client from './client'

export const postsApi = {
  /** Danh sách bài viết đã đăng (trang Tin tức) */
  list(params = {}) {
    return client.get('/posts/', { params }).then((r) => r.data)
  },

  /** Chi tiết 1 bài viết theo slug */
  detail(slug) {
    return client.get(`/posts/${slug}`).then((r) => r.data)
  },

  /** Vài bài khác để gợi ý cuối trang chi tiết */
  related(slug, limit = 2) {
    return client.get(`/posts/${slug}/related`, { params: { limit } }).then((r) => r.data)
  },
}
