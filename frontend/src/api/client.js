import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 15_000,
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT token to every request
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('huyvo_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Global response error handler
client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('huyvo_token')
      localStorage.removeItem('huyvo_user')
      // redirect to home if token expired mid-session
      if (window.location.pathname !== '/') window.location.href = '/'
    }
    return Promise.reject(err)
  },
)

export default client
