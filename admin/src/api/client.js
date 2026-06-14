import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

client.interceptors.request.use(cfg => {
  const token = localStorage.getItem('admin_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

client.interceptors.response.use(
  r => r.data,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      window.location.href = '/login'
    }
    return Promise.reject(err.response?.data?.detail || err.message)
  }
)

export default client
