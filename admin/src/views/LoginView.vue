<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-logo">
        <span class="logo-badge">RBD</span>
        <h1>Robin Admin</h1>
        <p>Đăng nhập để quản trị hệ thống</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input v-model="email" type="email" class="form-input" placeholder="admin@huyvo.com" required autofocus />
        </div>
        <div class="form-group">
          <label class="form-label">Mật khẩu</label>
          <input v-model="password" type="password" class="form-input" placeholder="••••••••" required />
        </div>

        <div v-if="errorMsg" class="error-box">{{ errorMsg }}</div>

        <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
          <span v-if="loading">Đang đăng nhập...</span>
          <span v-else>Đăng nhập</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const router    = useRouter()
const authStore = useAuthStore()

const email    = ref('')
const password = ref('')
const loading  = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  loading.value  = true
  errorMsg.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    errorMsg.value = typeof e === 'string' ? e : 'Email hoặc mật khẩu không đúng'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
  width: 100%;
  max-width: 400px;
  padding: 40px;
}

.login-logo {
  text-align: center;
  margin-bottom: 32px;
}
.logo-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px; height: 52px;
  background: var(--brand);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  border-radius: 14px;
  margin-bottom: 16px;
}
.login-logo h1 { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.login-logo p  { font-size: 13px; color: var(--text-2); }

.login-form .form-group { margin-bottom: 18px; }

.error-box {
  background: #FEE2E2;
  color: #991B1B;
  border: 1px solid #FECACA;
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 13px;
  margin-bottom: 16px;
}

.login-btn { width: 100%; justify-content: center; padding: 11px; font-size: 14px; }
</style>
