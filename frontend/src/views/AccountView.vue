<template>
  <div class="acc-page">
    <div class="acc-wrapper">

      <h1 class="acc-title">TÀI KHOẢN</h1>

      <!-- ── Đã đăng nhập ─────────────────────────────── -->
      <section v-if="auth.isLoggedIn" class="acc-dash">
        <div class="dash-card">
          <p class="dash-hello">
            Xin chào <strong>{{ auth.user?.full_name || auth.user?.email }}</strong>
          </p>
          <ul class="dash-info">
            <li><span>Họ và tên</span><b>{{ auth.user?.full_name || '—' }}</b></li>
            <li><span>Địa chỉ email</span><b>{{ auth.user?.email }}</b></li>
            <li><span>Số điện thoại</span><b>{{ auth.user?.phone || '—' }}</b></li>
          </ul>
          <div class="dash-actions">
            <RouterLink to="/cua-hang" class="btn-primary">TIẾP TỤC MUA SẮM</RouterLink>
            <button class="btn-ghost" @click="auth.logout()">ĐĂNG XUẤT</button>
          </div>
        </div>
      </section>

      <!-- ── Chưa đăng nhập ───────────────────────────── -->
      <div v-else class="acc-single">
        <Transition name="slide-up" mode="out-in">

          <!-- Đăng nhập -->
          <section v-if="mode === 'login'" key="login" class="acc-card">
            <h2 class="card-title">Đăng nhập</h2>

            <form class="acc-form" @submit.prevent="submitLogin">
              <label class="field">
                <span class="field-label">Tên tài khoản hoặc địa chỉ email <i>*</i></span>
                <input v-model.trim="loginForm.email" type="text" required autocomplete="username" />
              </label>

              <label class="field">
                <span class="field-label">Mật khẩu <i>*</i></span>
                <input v-model="loginForm.password" type="password" required autocomplete="current-password" />
              </label>

              <label class="checkbox">
                <input type="checkbox" v-model="loginForm.remember" />
                <span>Ghi nhớ mật khẩu</span>
              </label>

              <p v-if="loginError" class="form-error">{{ loginError }}</p>

              <button class="btn-primary" type="submit" :disabled="loginBusy">
                {{ loginBusy ? 'ĐANG XỬ LÝ...' : 'ĐĂNG NHẬP' }}
              </button>

              <button class="link-btn" type="button" @click="forgotHint = true">Quên mật khẩu?</button>
              <p v-if="forgotHint" class="form-hint">
                Liên hệ hotline hoặc email của cửa hàng để được hỗ trợ đặt lại mật khẩu.
              </p>

              <p class="switch-note">
                Chưa có tài khoản?
                <button type="button" class="switch-link" @click="switchTo('register')">Đăng ký ngay</button>
              </p>
            </form>
          </section>

          <!-- Đăng ký -->
          <section v-else key="register" class="acc-card">
            <h2 class="card-title">Đăng ký</h2>

            <form class="acc-form" @submit.prevent="submitRegister">
              <label class="field">
                <span class="field-label">Họ và tên</span>
                <input v-model.trim="registerForm.full_name" type="text" autocomplete="name" />
              </label>

              <label class="field">
                <span class="field-label">Số điện thoại</span>
                <input v-model.trim="registerForm.phone" type="tel" autocomplete="tel" />
              </label>

              <label class="field">
                <span class="field-label">Địa chỉ email <i>*</i></span>
                <input v-model.trim="registerForm.email" type="email" required autocomplete="email" />
              </label>

              <label class="field">
                <span class="field-label">Mật khẩu <i>*</i></span>
                <input v-model="registerForm.password" type="password" required minlength="6" autocomplete="new-password" />
              </label>

              <p v-if="registerError" class="form-error">{{ registerError }}</p>

              <button class="btn-primary" type="submit" :disabled="registerBusy">
                {{ registerBusy ? 'ĐANG XỬ LÝ...' : 'ĐĂNG KÝ' }}
              </button>

              <p class="switch-note">
                Đã có tài khoản?
                <button type="button" class="switch-link" @click="switchTo('login')">Đăng nhập</button>
              </p>
            </form>
          </section>

        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth   = useAuthStore()
const route  = useRoute()
const router = useRouter()

/** 'login' khi mới vào trang, đổi qua 'register' khi bấm "Đăng ký ngay" */
const mode = ref('login')

function switchTo(next) {
  if (mode.value === next) return
  mode.value = next
  loginError.value = registerError.value = ''
  forgotHint.value = false
}

const loginForm = reactive({ email: '', password: '', remember: true })
const loginBusy  = ref(false)
const loginError = ref('')
const forgotHint = ref(false)

const registerForm = reactive({ full_name: '', phone: '', email: '', password: '' })
const registerBusy  = ref(false)
const registerError = ref('')

/** Sau khi đăng nhập / đăng ký: quay lại trang trước đó nếu có ?redirect= */
function afterAuth() {
  const back = route.query.redirect
  if (typeof back === 'string' && back.startsWith('/')) router.push(back)
}

async function submitLogin() {
  loginError.value = ''
  loginBusy.value  = true
  try {
    await auth.login(loginForm.email, loginForm.password)
    afterAuth()
  } catch (e) {
    loginError.value = e?.response?.data?.detail || 'Đăng nhập không thành công.'
  } finally {
    loginBusy.value = false
  }
}

async function submitRegister() {
  registerError.value = ''
  registerBusy.value  = true
  try {
    await auth.register({ ...registerForm })
    afterAuth()
  } catch (e) {
    registerError.value = e?.response?.data?.detail || 'Đăng ký không thành công.'
  } finally {
    registerBusy.value = false
  }
}

</script>

<style scoped>
.acc-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: 100px 0 72px;
}

.acc-wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 48px;
}

.acc-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--brand-red);
  margin: 0 0 32px;
}

/* ── Card đơn: đăng nhập ↔ đăng ký ──────────────────── */
.acc-single {
  max-width: 520px;
  margin: 0 auto;
  overflow: hidden;   /* giữ animation trượt gọn trong khung */
}

/* Trượt từ dưới lên khi đổi giữa 2 form */
.slide-up-enter-active { transition: opacity .32s ease, transform .32s cubic-bezier(.25,.46,.45,.94); }
.slide-up-leave-active { transition: opacity .2s ease,  transform .2s  cubic-bezier(.25,.46,.45,.94); }
.slide-up-enter-from { opacity: 0; transform: translateY(40px); }
.slide-up-leave-to   { opacity: 0; transform: translateY(-24px); }

.acc-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 32px 32px 36px;
}

.card-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--brand-red);
  padding-bottom: 16px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

/* ── Form ───────────────────────────────────────────── */
.acc-form { display: flex; flex-direction: column; gap: 18px; }

.field { display: flex; flex-direction: column; gap: 8px; }

.field-label {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-dark);
}
.field-label i { color: var(--brand-red); font-style: normal; }

.field input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--warm-white);
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--text-dark);
  outline: none;
  transition: border-color var(--transition), background var(--transition);
}
.field input:focus { border-color: var(--brand-red); background: #fff; }

.checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-dark);
  cursor: pointer;
}
.checkbox input { accent-color: var(--brand-red); width: 16px; height: 16px; }

.btn-primary {
  display: inline-block;
  width: 100%;
  padding: 15px;
  background: var(--brand-red);
  border: 1px solid var(--brand-red);
  border-radius: 999px;
  color: #fff;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}
.btn-primary:hover { background: var(--brand-dark); border-color: var(--brand-dark); }
.btn-primary:disabled { opacity: .6; cursor: default; }

.btn-ghost {
  width: 100%;
  padding: 14px;
  background: #fff;
  border: 1.5px solid var(--brand-red);
  border-radius: 999px;
  color: var(--brand-red);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}
.btn-ghost:hover { background: var(--brand-red); color: #fff; }

.link-btn {
  align-self: flex-start;
  background: none;
  border: none;
  padding: 0;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-muted);
  text-decoration: underline;
  cursor: pointer;
  transition: color var(--transition);
}
.link-btn:hover { color: var(--brand-red); }

.form-error {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--brand-red);
  background: var(--cream);
  border-radius: 6px;
  padding: 10px 14px;
}

.form-hint {
  font-family: var(--font-body);
  font-size: 13px;
  font-style: italic;
  color: var(--text-muted);
}

.switch-note {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-muted);
}
.switch-link {
  background: none;
  border: none;
  padding: 0;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--brand-red);
  text-decoration: underline;
  cursor: pointer;
  transition: color var(--transition);
}
.switch-link:hover { color: var(--brand-dark); }

/* ── Dashboard khi đã đăng nhập ─────────────────────── */
.dash-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 32px;
  max-width: 640px;
}

.dash-hello {
  font-family: var(--font-display);
  font-size: 20px;
  color: var(--text-dark);
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--border);
}
.dash-hello strong { color: var(--brand-red); }

.dash-info { list-style: none; display: flex; flex-direction: column; gap: 14px; margin-bottom: 28px; }
.dash-info li {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  font-family: var(--font-body);
  font-size: 15px;
}
.dash-info span { color: var(--text-muted); }
.dash-info b { color: var(--text-dark); font-weight: 600; }

.dash-actions { display: flex; gap: 14px; }
.dash-actions > * { flex: 1; }

@media (max-width: 860px) {
  .acc-wrapper { padding: 0 20px; }
  .acc-card { padding: 26px 22px 30px; }
  .dash-actions { flex-direction: column; }
}
</style>
