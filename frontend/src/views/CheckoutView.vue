<template>
  <div class="checkout-page">
    <div class="checkout-layout">

      <!-- ── LEFT: Form ─────────────────────────────────────────── -->
      <div class="checkout-left">

        <!-- Thông tin thanh toán -->
        <section class="co-section">
          <h2 class="co-section-title">THÔNG TIN THANH TOÁN</h2>
          <form @submit.prevent="handleSubmit" novalidate>

            <div class="form-group">
              <label class="form-label">Email *</label>
              <input v-model="form.email" type="email" class="form-input"
                :class="{ error: errors.email }" placeholder="example@email.com" />
              <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Họ và tên*</label>
                <input v-model="form.full_name" type="text" class="form-input"
                  :class="{ error: errors.full_name }" />
                <span v-if="errors.full_name" class="form-error">{{ errors.full_name }}</span>
              </div>
              <div class="form-group">
                <label class="form-label">Số điện thoại*</label>
                <input v-model="form.phone" type="tel" class="form-input"
                  :class="{ error: errors.phone }" />
                <span v-if="errors.phone" class="form-error">{{ errors.phone }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Quốc gia/Khu vực *</label>
                <select v-model="form.country" class="form-input form-select">
                  <option value="Vietnam">Việt Nam</option>
                  <option value="US">Hoa Kỳ</option>
                  <option value="JP">Nhật Bản</option>
                  <option value="KR">Hàn Quốc</option>
                  <option value="SG">Singapore</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Tỉnh / Thành phố *</label>
                <select v-model="form.city" class="form-input form-select"
                  :class="{ error: errors.city }" :disabled="loadingProvinces">
                  <option value="">{{ loadingProvinces ? 'Đang tải...' : 'Chọn Tỉnh / Thành phố' }}</option>
                  <option v-for="p in provinces" :key="p.code" :value="p.name">{{ p.name }}</option>
                </select>
                <span v-if="errors.city" class="form-error">{{ errors.city }}</span>
                <span v-if="locationError" class="form-error">
                  {{ locationError }} <a href="#" @click.prevent="loadProvinces">Thử lại</a>
                </span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Phường / Xã *</label>
                <select v-model="form.ward" class="form-input form-select"
                  :class="{ error: errors.ward }" :disabled="!form.city || loadingWards">
                  <option value="">{{ loadingWards ? 'Đang tải...' : 'Chọn Phường / Xã' }}</option>
                  <option v-for="w in wardsList" :key="w.code" :value="w.name">{{ w.name }}</option>
                </select>
                <span v-if="errors.ward" class="form-error">{{ errors.ward }}</span>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Địa chỉ *</label>
              <input v-model="form.address" type="text" class="form-input"
                placeholder="Địa chỉ" :class="{ error: errors.address }" />
              <span v-if="errors.address" class="form-error">{{ errors.address }}</span>
            </div>

            <div class="form-group">
              <label class="form-label">Ghi chú đơn hàng (tùy chọn)</label>
              <textarea v-model="form.note" class="form-input form-textarea"
                placeholder="Ghi chú về đơn hàng, ví dụ thời gian hay địa điểm giao hàng chi tiết hơn." rows="4" />
            </div>

          </form>
        </section>

        <!-- Thông tin giao hàng -->
        <section class="co-section">
          <h2 class="co-section-title co-section-title--dark">THÔNG TIN GIAO HÀNG</h2>
          <div class="shipping-info-box">
            Giao hàng tiêu chuẩn: 1 - 3 ngày qua Viettel Post
          </div>
        </section>

        <!-- Phương thức thanh toán -->
        <section class="co-section">
          <h2 class="co-section-title co-section-title--dark">PHƯƠNG THỨC THANH TOÁN</h2>
          <div class="payment-box">

            <!-- OnePay -->
            <label class="payment-option" :class="{ selected: payMethod === 'onepay' }">
              <input type="radio" v-model="payMethod" value="onepay" />
              <span class="payment-name">OnePay</span>
              <div class="card-logos">
                <span class="card-logo visa">VISA</span>
                <span class="card-logo master">MC</span>
                <span class="card-logo amex">AMEX</span>
                <span class="card-logo jcb">JCB</span>
                <span class="card-logo union">UP</span>
              </div>
            </label>
            <Transition name="pay-detail">
              <div v-if="payMethod === 'onepay'" class="payment-detail">
                Nhấp vào "Đặt hàng" và bạn sẽ được chuyển đến trang web OnePAY để thanh toán.
              </div>
            </Transition>

            <div class="payment-divider" />

            <!-- Bank transfer -->
            <label class="payment-option" :class="{ selected: payMethod === 'bank' }">
              <input type="radio" v-model="payMethod" value="bank" />
              <span class="payment-name">Chuyển khoản ngân hàng</span>
              <span v-if="payMethod === 'bank'" class="payment-name-sub">với mã QR</span>
            </label>

          </div>

          <!-- Bank transfer detail -->
          <Transition name="pay-detail">
            <div v-if="payMethod === 'bank'" class="bank-wrap">
              <p class="bank-note">
                Bấm <strong>Đặt hàng</strong> để nhận mã QR kèm sẵn số tiền cọc và nội dung
                chuyển khoản. Quét bằng ứng dụng ngân hàng là xong — hệ thống tự ghi nhận
                khi tiền về, không cần gửi ảnh xác nhận.
              </p>
              <ul class="bank-steps">
                <li>Số tiền cọc: <strong>{{ formatPrice(depositAmount) }}</strong> (50% giá trị đơn)</li>
                <li>Phần còn lại thanh toán khi nhận hàng</li>
              </ul>
            </div>
          </Transition>
        </section>

        <!-- Agreement + Submit -->
        <div class="co-footer">
          <label class="agree-label">
            <input type="checkbox" v-model="agreed" />
            <span>Tôi đã đọc và đồng ý với điều khoản và điều kiện của website <span class="required">*</span></span>
          </label>
          <span v-if="errors.agreed" class="form-error">{{ errors.agreed }}</span>

          <div v-if="submitError" class="submit-error">{{ submitError }}</div>

          <button class="submit-btn" @click.prevent="handleSubmit" :disabled="submitting">
            <span v-if="submitting">Đang xử lý…</span>
            <span v-else>THANH TOÁN</span>
          </button>
        </div>

      </div>

      <!-- ── RIGHT: Order summary ───────────────────────────────── -->
      <div class="checkout-right">
        <h2 class="summary-title">ĐƠN HÀNG CỦA BẠN</h2>

        <div class="summary-items">
          <div v-if="!cartStore.items.length" class="summary-empty">Giỏ hàng trống</div>
          <div v-for="item in cartStore.items" :key="item._key" class="summary-item">
            <div class="item-img" :style="{ background: swatchGradient(item.color_hex) }" />
            <div class="item-info">
              <p class="item-name">{{ item.name.toUpperCase() }}</p>
              <p v-if="item.product_type === 'fabric'" class="item-detail">Bán theo {{ item.unit_label || 'mét' }}</p>
              <p v-else-if="item.tailoring_method === 'custom'" class="item-detail">May theo số đo</p>
              <p v-else class="item-detail">Size: {{ item.size }}</p>
              <p v-if="item.lining_type" class="item-detail">Tà trong: {{ item.lining_type === 'yem_roi' ? 'Yếm rời' : 'Liền tà ngoài' }}</p>
              <p v-if="item.color_option" class="item-detail">Màu sắc: {{ item.color_option === 'same' ? 'Giống ảnh mẫu' : 'Phối màu riêng' }}</p>
            </div>
            <div class="item-right">
              <span class="item-qty">
                x{{ formatQty(item.quantity) }}<em v-if="item.product_type === 'fabric'">{{ item.unit_label || 'mét' }}</em>
              </span>
              <span class="item-price">{{ formatPrice(item.price * item.quantity) }}</span>
            </div>
          </div>
        </div>

        <div class="summary-divider" />

        <div class="summary-totals">
          <div class="total-row">
            <span>Tạm tính</span>
            <span>{{ formatPrice(cartStore.total) }}</span>
          </div>
          <div class="total-row deposit">
            <span>Đặt cọc 50%</span>
            <span>{{ formatPrice(depositAmount) }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Success modal -->
    <Teleport to="body">
      <Transition name="overlay">
        <div v-if="success" class="success-overlay" />
      </Transition>
      <Transition name="modal">
        <div v-if="success" class="success-modal" role="dialog" aria-modal="true">
          <div class="success-icon">
            <svg viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="22" stroke="var(--brand-red)" stroke-width="1.5"/>
              <path d="M14 24l7 7 13-13" stroke="var(--brand-red)" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h2 class="success-title">{{ paid ? 'Đã nhận tiền cọc!' : 'Đặt hàng thành công!' }}</h2>
          <p class="success-sub">Mã đơn hàng: <strong>{{ orderCode }}</strong></p>

          <!-- Chuyển khoản: hiện mã QR rồi chờ ngân hàng báo về -->
          <div v-if="payMethod === 'bank' && !paid" class="pay-box">
            <p v-if="qrLoading" class="pay-loading">Đang tạo mã QR…</p>

            <template v-else-if="qr?.available">
              <img :src="qrImage" alt="Mã QR chuyển khoản" class="pay-qr" />
              <p class="pay-amount">{{ formatPrice(qr.deposit_amount) }}</p>
              <p class="pay-hint">Quét bằng ứng dụng ngân hàng — số tiền và nội dung đã điền sẵn.</p>
              <p class="pay-wait"><span class="pay-dot" />Đang chờ ngân hàng xác nhận…</p>
            </template>

            <!-- Chưa bật VietQR hoặc tạo QR lỗi → chuyển khoản tay -->
            <template v-else>
              <p class="pay-hint">{{ qr?.message || 'Vui lòng chuyển khoản theo thông tin dưới đây.' }}</p>
              <ul class="pay-manual">
                <li>Ngân hàng: <strong>{{ bankInfo.bank }}</strong></li>
                <li>Số tài khoản: <strong>{{ bankInfo.account }}</strong></li>
                <li>Chủ tài khoản: <strong>{{ bankInfo.holder }}</strong></li>
                <li>Số tiền: <strong>{{ formatPrice(qr?.deposit_amount ?? depositAmount) }}</strong></li>
                <li>Nội dung: <strong>{{ orderCode }}</strong></li>
              </ul>
              <button class="btn-copy" @click="copyOrderCode">Sao chép nội dung CK</button>
            </template>
          </div>

          <p v-else-if="paid" class="success-desc">
            Đã nhận <strong>{{ formatPrice(qr?.deposit_amount ?? depositAmount) }}</strong> tiền cọc.
            Chúng tôi sẽ liên hệ xác nhận sớm nhất.
          </p>
          <p v-else class="success-desc">Chúng tôi sẽ liên hệ xác nhận qua điện thoại sớm nhất.</p>

          <RouterLink to="/" class="success-btn">Về trang chủ</RouterLink>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { ordersApi, locationsApi, paymentsApi } from '@/api'

const cartStore = useCartStore()

/** 3.8 → "3,8" ; 2 → "2" */
const formatQty = (v) => Number(v).toLocaleString('vi-VN', { maximumFractionDigits: 1 })
const authStore = useAuthStore()

const payMethod = ref('onepay')
const agreed    = ref(false)

// Mã đơn do server cấp sau khi tạo đơn — đây cũng là nội dung chuyển khoản
// và orderId gửi sang VietQR, nên bắt buộc phải là mã thật chứ không random.
const orderCode = ref('')

const depositAmount = computed(() => Math.round(cartStore.total * 0.5))

// ── Thanh toán chuyển khoản qua VietQR ──────────────────────────────────
const qr        = ref(null)    // { qr_code, qr_link, available, message, ... }
const qrLoading = ref(false)
const paid      = ref(false)
let   pollTimer = null

async function startVietQr() {
  if (!orderCode.value) return
  qrLoading.value = true
  try {
    qr.value = await paymentsApi.vietqr(orderCode.value)
  } catch {
    qr.value = null
  } finally {
    qrLoading.value = false
  }
  pollPayment()
}

/** Hỏi server 5 giây một lần, tối đa 15 phút. */
function pollPayment() {
  let ticks = 0
  clearInterval(pollTimer)
  pollTimer = setInterval(async () => {
    ticks += 1
    if (ticks > 180) return clearInterval(pollTimer)
    try {
      const st = await paymentsApi.status(orderCode.value)
      if (st.payment_status === 'paid') {
        paid.value = true
        clearInterval(pollTimer)
      }
    } catch { /* mạng chập chờn thì bỏ qua, lần sau hỏi lại */ }
  }, 5000)
}

/** VietQR trả cả ảnh sẵn (qr_link) lẫn chuỗi QR — có ảnh thì dùng luôn. */
// Chưa cấu hình VietQR thì vẫn phải hiện đúng tài khoản như trước đây,
// không được để khách nhìn vào khối trống không biết chuyển đi đâu.
const BANK_FALLBACK = {
  bank:    'VPBank - Việt Nam Thịnh Vượng',
  account: '0886733714',
  holder:  'LÊ VĂN TUẤN',
}
const bankInfo = computed(() => ({
  bank:    qr.value?.bank_code    || BANK_FALLBACK.bank,
  account: qr.value?.bank_account || BANK_FALLBACK.account,
  holder:  qr.value?.account_name || BANK_FALLBACK.holder,
}))

const qrImage = computed(() => {
  if (qr.value?.qr_link) return qr.value.qr_link
  if (!qr.value?.qr_code) return ''
  return `https://api.vietqr.io/image/${encodeURIComponent(qr.value.qr_code)}`
})

onUnmounted(() => clearInterval(pollTimer))

const form = ref({
  email:     authStore.user?.email     ?? '',
  full_name: authStore.user?.full_name ?? '',
  phone:     authStore.user?.phone     ?? '',
  country:   'Vietnam',
  city:      '',
  ward:      '',
  address:   '',
  note:      '',
})

const errors      = ref({})
const submitting  = ref(false)
const submitError = ref('')
const success     = ref(false)

// ── Địa chỉ hành chính VN (tỉnh/thành → phường/xã) ──────────────────────
const provinces       = ref([])
const wardsList       = ref([])
const loadingProvinces = ref(false)
const loadingWards     = ref(false)
const locationError    = ref('')

async function loadProvinces() {
  loadingProvinces.value = true
  locationError.value = ''
  try {
    provinces.value = await locationsApi.provinces()
  } catch {
    locationError.value = 'Không tải được danh sách tỉnh/thành.'
  } finally {
    loadingProvinces.value = false
  }
}

watch(() => form.value.city, async (cityName) => {
  form.value.ward = ''
  wardsList.value = []
  if (!cityName) return
  const province = provinces.value.find((p) => p.name === cityName)
  if (!province) return
  loadingWards.value = true
  try {
    wardsList.value = await locationsApi.wards(province.code)
  } catch {
    locationError.value = 'Không tải được danh sách phường/xã.'
  } finally {
    loadingWards.value = false
  }
})

onMounted(loadProvinces)

function formatPrice(n) {
  return Number(n).toLocaleString('vi-VN') + ' Đ'
}
function swatchGradient(hex) {
  if (!hex) return 'linear-gradient(160deg,#ece5d5,#d4c8b0)'
  return `linear-gradient(160deg,${hex}44,${hex}88)`
}
function copyOrderCode() {
  navigator.clipboard?.writeText(orderCode.value)
}

function validate() {
  const e = {}
  if (!form.value.email.trim())     e.email     = 'Vui lòng nhập email'
  if (!form.value.full_name.trim()) e.full_name = 'Vui lòng nhập họ tên'
  if (!form.value.phone.trim())     e.phone     = 'Vui lòng nhập số điện thoại'
  if (!form.value.address.trim())   e.address   = 'Vui lòng nhập địa chỉ'
  if (!form.value.city)             e.city      = 'Vui lòng chọn tỉnh / thành'
  if (!form.value.ward)             e.ward      = 'Vui lòng chọn phường / xã'
  if (!agreed.value)                e.agreed    = 'Vui lòng đồng ý với điều khoản'
  errors.value = e
  return !Object.keys(e).length
}

async function handleSubmit() {
  submitError.value = ''
  if (!validate()) return
  if (!cartStore.count) { submitError.value = 'Giỏ hàng đang trống.'; return }
  submitting.value = true
  try {
    const order = await ordersApi.create({
      ...form.value,
      payment_method: payMethod.value,
      items: cartStore.toOrderItems?.() ?? [],
    })
    orderCode.value = order.order_code || ''
    cartStore.clear()
    success.value = true

    // Chuyển khoản → xin mã QR rồi chờ VietQR báo tiền về
    if (payMethod.value === 'bank') await startVietQr()
  } catch {
    submitError.value = 'Có lỗi xảy ra, vui lòng thử lại.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.checkout-page {
  background: #fff;
  min-height: 80vh;
  padding: var(--page-top) 0 80px;
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 60px;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 var(--page-x);
  align-items: start;
}

/* ── LEFT ──────────────────────────────────────────────── */
.checkout-left {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.co-section {}

.co-section-title {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--brand-red);
  margin-bottom: 20px;
}
.co-section-title--dark { color: var(--charcoal); }

/* Form */
form { display: flex; flex-direction: column; gap: 16px; }

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.form-group { display: flex; flex-direction: column; gap: 6px; }

.form-label {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-dark);
}

.form-input {
  border: 1px solid #D5D5D0;
  background: #fff;
  font-family: var(--font-body);
  font-size: 13px;
  padding: 10px 12px;
  color: var(--charcoal);
  outline: none;
  width: 100%;
  border-radius: 3px;
  transition: border-color var(--transition);
}
.form-input:focus { border-color: var(--charcoal); }
.form-input.error { border-color: #c0395a; }
.form-select { appearance: none; cursor: pointer; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23888' stroke-width='1.5' fill='none'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 32px; }
.form-textarea { resize: vertical; min-height: 100px; }
.form-error { font-size: 11px; color: #c0395a; }

/* Shipping info */
.shipping-info-box {
  border: 1px solid #D5D5D0;
  padding: 14px 16px;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  border-radius: 3px;
}

/* Payment */
.payment-box {
  border: 1px solid #D5D5D0;
  border-radius: 3px;
  overflow: hidden;
}
.payment-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 13px;
}
.payment-option input[type="radio"] { accent-color: var(--brand-red); }
.payment-name { flex: 1; color: var(--text-dark); }
.payment-name-sub { font-size: 12px; color: var(--brand-red); font-style: italic; }

.card-logos { display: flex; gap: 4px; align-items: center; }
.card-logo {
  font-size: 8px;
  font-weight: 700;
  padding: 3px 6px;
  border-radius: 3px;
  letter-spacing: .5px;
  color: #fff;
}
.visa   { background: #1A1F71; }
.master { background: #EB001B; }
.amex   { background: #2E77BC; }
.jcb    { background: #003087; }
.union  { background: #B22222; }

.payment-detail {
  background: #F5F3EF;
  padding: 12px 16px;
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.6;
  margin: 0 16px 14px;
  border-radius: 3px;
}
.payment-divider { height: 1px; background: #D5D5D0; }

/* Bank transfer */
.bank-wrap { margin-top: 20px; }
.bank-steps { margin: 12px 0 0 18px; font-size: 13px; line-height: 1.9; color: var(--text-dark); }

/* Khối thanh toán trong popup đặt hàng thành công */
.pay-box { margin: 18px 0 8px; }
.pay-loading { font-size: 13px; color: var(--text-muted); padding: 24px 0; }
.pay-qr {
  width: 220px; height: 220px; margin: 0 auto;
  border: 1px solid var(--border); border-radius: 10px; background: #fff;
}
.pay-amount {
  font-family: var(--font-display); font-size: 22px;
  color: var(--brand-red); margin-top: 12px;
}
.pay-hint { font-size: 13px; color: var(--text-muted); line-height: 1.7; margin-top: 6px; }
.pay-wait {
  display: inline-flex; align-items: center; gap: 8px;
  margin-top: 14px; font-size: 13px; color: var(--text-dark);
}
.pay-dot {
  width: 8px; height: 8px; border-radius: 50%; background: var(--brand-red);
  animation: pay-pulse 1.2s ease-in-out infinite;
}
@keyframes pay-pulse { 0%,100% { opacity: .25 } 50% { opacity: 1 } }

.pay-manual {
  list-style: none; margin: 14px 0; padding: 14px 16px;
  background: var(--warm-white); border-radius: 8px;
  font-size: 13px; line-height: 2; text-align: left;
}
.bank-note {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  margin-bottom: 16px;
  line-height: 1.6;
}
.bank-card {
  border: 1px solid #D5D5D0;
  border-radius: 6px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  overflow: hidden;
}
.bank-info {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-right: 1px solid #D5D5D0;
}
.bank-info p {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  line-height: 1.5;
}
.bank-info strong { font-weight: 600; }
.bank-highlight { color: #1565C0; }
.btn-copy {
  margin-top: 8px;
  padding: 8px 16px;
  border: 1px solid #D5D5D0;
  background: #fff;
  border-radius: 4px;
  font-family: var(--font-body);
  font-size: 12px;
  cursor: pointer;
  color: var(--text-dark);
  transition: background var(--transition);
  width: fit-content;
}
.btn-copy:hover { background: #f5f5f5; }

.bank-qr {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.qr-placeholder {
  width: 140px;
  height: 140px;
}
.qr-placeholder svg { width: 100%; height: 100%; }
.qr-caption {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
}
.btn-qr {
  padding: 8px 24px;
  background: #1565C0;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-family: var(--font-body);
  font-size: 12px;
  cursor: pointer;
  transition: opacity var(--transition);
}
.btn-qr:hover { opacity: .85; }

/* Footer */
.co-footer { display: flex; flex-direction: column; gap: 12px; }

.agree-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  cursor: pointer;
}
.agree-label input { accent-color: var(--brand-red); margin-top: 2px; flex-shrink: 0; }
.required { color: var(--brand-red); }

.submit-error {
  background: #fdf0f2;
  border: 1px solid #f8d7da;
  color: #c0395a;
  padding: 10px 14px;
  font-size: 13px;
  border-radius: 3px;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: var(--brand-red);
  border: none;
  color: #fff;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  cursor: pointer;
  transition: background var(--transition);
  border-radius: 2px;
}
.submit-btn:hover:not(:disabled) { background: var(--brand-dark); }
.submit-btn:disabled { opacity: .5; cursor: not-allowed; }

/* ── RIGHT ─────────────────────────────────────────────── */
.checkout-right {
  position: sticky;
  top: 84px;
}

.summary-title {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--brand-red);
  margin-bottom: 24px;
}

.summary-items { display: flex; flex-direction: column; gap: 20px; }

.summary-empty {
  font-size: 13px;
  color: var(--text-muted);
  padding: 16px 0;
}

.summary-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.item-img {
  width: 72px;
  height: 96px;
  border-radius: 6px;
  flex-shrink: 0;
}

.item-info { flex: 1; }

.item-name {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 700;
  color: var(--charcoal);
  line-height: 1.4;
  margin-bottom: 6px;
  letter-spacing: .5px;
}

.item-detail {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--brand-red);
  line-height: 1.6;
}

.item-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex-shrink: 0;
}
.item-qty {
  font-size: 12px;
  color: var(--text-muted);
}
.item-qty em { font-style: normal; margin-left: 3px; }
.item-price {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  color: var(--charcoal);
  white-space: nowrap;
}

.summary-divider {
  height: 1px;
  background: #D5D5D0;
  margin: 20px 0;
}

.summary-totals { display: flex; flex-direction: column; gap: 12px; }

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-dark);
}

.total-row.deposit {
  font-weight: 700;
  font-size: 16px;
  color: var(--charcoal);
}

/* Transitions */
.pay-detail-enter-active, .pay-detail-leave-active {
  transition: max-height .3s ease, opacity .25s ease;
  overflow: hidden;
  max-height: 400px;
}
.pay-detail-enter-from, .pay-detail-leave-to { max-height: 0; opacity: 0; }

/* Success */
.success-overlay {
  position: fixed; inset: 0;
  background: rgba(26,26,24,.55);
  z-index: 1200;
  backdrop-filter: blur(3px);
}
.success-modal {
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%,-50%);
  width: 460px; max-width: calc(100vw - 32px);
  background: #fff; z-index: 1201;
  padding: 52px 44px; text-align: center;
  border-radius: 4px;
}
.success-icon svg { width: 64px; height: 64px; margin-bottom: 20px; }
.success-title {
  font-family: var(--font-display);
  font-size: 28px; font-weight: 400;
  margin-bottom: 10px; color: var(--charcoal);
}
.success-sub { font-size: 14px; color: var(--text-muted); margin-bottom: 8px; }
.success-sub strong { color: var(--brand-red); }
.success-desc { font-size: 13px; color: var(--text-muted); line-height: 1.7; margin-bottom: 28px; }
.success-btn {
  display: inline-block; padding: 13px 36px;
  background: var(--brand-red); color: #fff;
  font-family: var(--font-body); font-size: 11px;
  font-weight: 600; letter-spacing: 3px; text-transform: uppercase;
  border-radius: 2px; transition: background var(--transition);
}
.success-btn:hover { background: var(--brand-dark); }
.overlay-enter-active, .overlay-leave-active { transition: opacity .3s; }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }
.modal-enter-active, .modal-leave-active { transition: opacity .3s, transform .3s; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: translate(-50%,-46%); }

/* ══ Responsive ═══════════════════════════════════════════════════════ */
@media (max-width: 900px) {
  /* Tóm tắt đơn lên trên để khách thấy ngay tổng tiền, form nhập xuống dưới */
  .checkout-layout { grid-template-columns: 1fr; gap: 34px; }
  .checkout-right  { position: static; order: -1; }
  .checkout-left   { gap: 28px; }
}
@media (max-width: 560px) {
  .checkout-page { padding-bottom: 56px; }
  .form-row  { grid-template-columns: 1fr; gap: 14px; }
  .bank-card { grid-template-columns: 1fr; }
  .bank-info { border-right: none; border-bottom: 1px solid #D5D5D0; padding: 16px 18px; }
  .co-section-title { font-size: 12px; letter-spacing: 1.5px; }
}
</style>
