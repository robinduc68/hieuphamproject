<template>
  <section class="newsletter">
    <div class="newsletter-inner">
      <div class="newsletter-deco" aria-hidden="true">
        <svg viewBox="0 0 160 320" fill="none" class="deco-svg">
          <line x1="80" y1="0" x2="80" y2="320" stroke="var(--gold)" stroke-width=".6" opacity=".2"/>
          <circle cx="80" cy="60" r="4" fill="var(--gold)" opacity=".3"/>
          <circle cx="80" cy="160" r="6" fill="var(--gold)" opacity=".2"/>
          <circle cx="80" cy="260" r="4" fill="var(--gold)" opacity=".3"/>
          <rect x="20" y="130" width="120" height="60" stroke="var(--gold)" stroke-width=".5" opacity=".12"/>
        </svg>
      </div>

      <div class="newsletter-content">
        <span class="section-label" style="text-align:center;display:block">Cộng Đồng HUY VO</span>
        <h2 class="newsletter-title">Đăng ký để luôn<br/><em>cập nhật mới nhất</em></h2>
        <p class="newsletter-desc">
          Nhận thông tin về các bộ sưu tập mới, sự kiện độc quyền và ưu đãi dành riêng cho thành viên HUY VO.
        </p>

        <form class="newsletter-form" @submit.prevent="handleSubmit" novalidate>
          <div class="form-row">
            <input v-model="name" type="text" placeholder="Họ và tên" class="form-input" />
            <div class="input-group">
              <input v-model="email" type="email" placeholder="Địa chỉ email *" class="form-input" :class="{ error: emailError }" required />
              <span v-if="emailError" class="input-error">{{ emailError }}</span>
            </div>
          </div>
          <label class="checkbox-label">
            <input v-model="consent" type="checkbox" class="sr-only" />
            <span class="checkbox-custom" :class="{ checked: consent }">
              <svg v-if="consent" viewBox="0 0 12 10" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 5l3 3 7-7"/></svg>
            </span>
            <span class="checkbox-text">Tôi đồng ý nhận thông tin từ <strong>HUY VO</strong>.</span>
          </label>
          <button type="submit" class="submit-btn" :disabled="submitting || submitted">
            <span v-if="submitting">Đang xử lý…</span>
            <span v-else-if="submitted" class="submitted-text">
              <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              Đã đăng ký thành công!
            </span>
            <span v-else>Đăng Ký Ngay</span>
          </button>
          <p v-if="apiError" class="api-error">{{ apiError }}</p>
        </form>
      </div>

      <div class="newsletter-deco" aria-hidden="true">
        <svg viewBox="0 0 160 320" fill="none" class="deco-svg" style="transform:scaleX(-1)">
          <line x1="80" y1="0" x2="80" y2="320" stroke="var(--gold)" stroke-width=".6" opacity=".2"/>
          <circle cx="80" cy="60" r="4" fill="var(--gold)" opacity=".3"/>
          <circle cx="80" cy="160" r="6" fill="var(--gold)" opacity=".2"/>
          <circle cx="80" cy="260" r="4" fill="var(--gold)" opacity=".3"/>
          <rect x="20" y="130" width="120" height="60" stroke="var(--gold)" stroke-width=".5" opacity=".12"/>
        </svg>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { newsletterApi } from '@/api'

const name       = ref('')
const email      = ref('')
const consent    = ref(false)
const emailError = ref('')
const submitting = ref(false)
const submitted  = ref(false)
const apiError   = ref('')

async function handleSubmit() {
  emailError.value = ''
  apiError.value   = ''
  if (!email.value || !/\S+@\S+\.\S+/.test(email.value)) {
    emailError.value = 'Vui lòng nhập địa chỉ email hợp lệ.'
    return
  }
  submitting.value = true
  try {
    await newsletterApi.subscribe(email.value, name.value || undefined)
    submitted.value = true
    name.value = ''
    email.value = ''
    consent.value = false
    setTimeout(() => { submitted.value = false }, 5000)
  } catch (e) {
    apiError.value = e?.response?.data?.detail ?? 'Có lỗi xảy ra, vui lòng thử lại.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.newsletter { background: var(--charcoal); padding: 96px var(--page-x); overflow: hidden; }
.newsletter-inner { max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: 160px 1fr 160px; gap: 48px; align-items: center; }
.newsletter-deco { display: flex; align-items: center; justify-content: center; }
.deco-svg { width: 100%; height: 320px; }
.newsletter-content { text-align: center; }
.newsletter-title { font-family: var(--font-display); font-size: clamp(32px,4vw,52px); font-weight: 300; color: var(--cream); line-height: 1.1; margin-bottom: 20px; }
.newsletter-title em { font-style: italic; color: var(--gold-light); }
.newsletter-desc { font-size: 13px; line-height: 1.85; color: rgba(245,240,232,.55); margin-bottom: 40px; max-width: 480px; margin-left: auto; margin-right: auto; }
.newsletter-form { display: flex; flex-direction: column; gap: 16px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.input-group { position: relative; }
.form-input { width: 100%; background: rgba(245,240,232,.06); border: 1px solid rgba(245,240,232,.12); color: var(--cream); font-family: var(--font-body); font-size: 12px; letter-spacing: 1px; padding: 14px 18px; outline: none; transition: border-color var(--transition); }
.form-input::placeholder { color: rgba(245,240,232,.25); }
.form-input:focus { border-color: rgba(184,151,42,.5); }
.form-input.error { border-color: #c0395a; }
.input-error { position: absolute; bottom: -18px; left: 0; font-size: 10px; color: #e05070; letter-spacing: .5px; }
.checkbox-label { display: flex; align-items: flex-start; gap: 12px; cursor: pointer; text-align: left; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
.checkbox-custom { width: 18px; height: 18px; flex-shrink: 0; border: 1px solid rgba(245,240,232,.25); display: flex; align-items: center; justify-content: center; margin-top: 2px; transition: background var(--transition), border-color var(--transition); }
.checkbox-custom.checked { background: var(--gold); border-color: var(--gold); }
.checkbox-custom svg { width: 10px; height: 10px; color: var(--charcoal); }
.checkbox-text { font-size: 11px; line-height: 1.6; color: rgba(245,240,232,.45); }
.submit-btn { background: var(--gold); border: none; color: var(--charcoal); font-family: var(--font-body); font-size: 11px; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; padding: 16px; transition: opacity var(--transition); display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; }
.submit-btn:hover:not(:disabled) { background: var(--gold-light); }
.submit-btn:disabled { opacity: .75; cursor: default; }
.submitted-text { display: flex; align-items: center; gap: 10px; }
.api-error { font-size: 11px; color: #e05070; text-align: center; }

@media (max-width: 900px) {
  .newsletter { padding: 60px var(--page-x); }
  .newsletter-inner { grid-template-columns: 1fr; gap: 24px; text-align: center; }
}
@media (max-width: 560px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
