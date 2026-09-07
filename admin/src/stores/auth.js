import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('admin_token') || '')
  const user  = ref(JSON.parse(localStorage.getItem('admin_user') || 'null'))

  const isLoggedIn = computed(() => !!token.value && user.value?.is_admin)

  // Quyền do backend tính sẵn và trả kèm tài khoản (app/permissions.py).
  const permissions = computed(() => user.value?.permissions ?? [])

  /** can('products.create') — dùng để ẩn tab và nút trong trang admin. */
  function can(...codes) {
    return codes.some(code => permissions.value.includes(code))
  }

  /**
   * Nạp lại tài khoản từ server. Cần cho phiên đăng nhập cũ: bản lưu trong
   * localStorage chưa có danh sách quyền.
   */
  async function refresh() {
    if (!token.value) return
    try {
      const me = await authApi.me()
      user.value = me
      localStorage.setItem('admin_user', JSON.stringify(me))
    } catch {
      // token hết hạn / bị khoá → client.js đã tự đẩy về /login
    }
  }

  async function login(email, password) {
    const data = await authApi.login({ email, password })
    if (!data.user.is_admin) throw new Error('Tài khoản không có quyền admin')
    token.value = data.access_token
    user.value  = data.user
    localStorage.setItem('admin_token', data.access_token)
    localStorage.setItem('admin_user', JSON.stringify(data.user))
  }

  function logout() {
    token.value = ''
    user.value  = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
  }

  return { token, user, isLoggedIn, permissions, can, refresh, login, logout }
})
