import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import { useAuthStore } from '@/stores/auth.js'
import '@/assets/admin.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

// Nạp lại quyền trước khi vẽ giao diện — phiên đăng nhập cũ trong localStorage
// chưa có danh sách quyền nên sẽ không thấy tab nào.
useAuthStore().refresh().finally(() => app.mount('#app'))
