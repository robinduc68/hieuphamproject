import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usersApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('huyvo_token') || null)
  const user  = ref(JSON.parse(localStorage.getItem('huyvo_user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin    = computed(() => user.value?.is_admin === true)

  function _persist(data) {
    token.value = data.access_token
    user.value  = data.user
    localStorage.setItem('huyvo_token', data.access_token)
    localStorage.setItem('huyvo_user',  JSON.stringify(data.user))
  }

  async function register(payload) {
    const data = await usersApi.register(payload)
    _persist(data)
    return data
  }

  async function login(email, password) {
    const data = await usersApi.login(email, password)
    _persist(data)
    return data
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const me = await usersApi.me()
      user.value = me
      localStorage.setItem('huyvo_user', JSON.stringify(me))
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('huyvo_token')
    localStorage.removeItem('huyvo_user')
  }

  return { token, user, isLoggedIn, isAdmin, register, login, fetchMe, logout }
})
