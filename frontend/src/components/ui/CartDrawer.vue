<template>
  <Teleport to="body">
    <Transition name="overlay">
      <div v-if="open" class="cart-overlay" @click="$emit('close')" />
    </Transition>
    <Transition name="drawer">
      <aside v-if="open" class="cart-drawer" role="dialog" aria-modal="true" aria-label="Giỏ hàng">
        <div class="cart-header">
          <h2 class="cart-title">Giỏ Hàng <span class="cart-count">({{ cartStore.count }})</span></h2>
          <button class="cart-close" @click="$emit('close')" aria-label="Đóng">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="cart-body">
          <div v-if="cartStore.count === 0" class="cart-empty">
            <div class="cart-empty-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
                <line x1="3" y1="6" x2="21" y2="6"/>
                <path d="M16 10a4 4 0 01-8 0"/>
              </svg>
            </div>
            <p class="cart-empty-text">Không có sản phẩm trong giỏ hàng.</p>
            <RouterLink to="/cua-hang" class="cart-shop-link" @click="$emit('close')">Khám phá sản phẩm</RouterLink>
          </div>

          <div v-else class="cart-items">
            <div v-for="item in cartStore.items" :key="item._key" class="cart-item">
              <div class="ci-img" :style="{ background: swatchGrad(item.color_hex) }" />
              <div class="ci-info">
                <p class="ci-name">{{ item.name }}</p>
                <p v-if="item.tailoring_method !== 'custom'" class="ci-meta">Size: {{ item.size }}</p>
                <p v-else class="ci-meta">May theo số đo</p>
                <p v-if="item.lining_type" class="ci-meta">Tà trong: {{ item.lining_type === 'yem_roi' ? 'Yếm rời' : 'Liền tà' }}</p>
                <p v-if="item.color_option" class="ci-meta">Màu: {{ item.color_option === 'same' ? 'Giống ảnh' : 'Phối màu riêng' }}</p>
                <div class="ci-qty">
                  <button @click="cartStore.updateQty(item._key, item.quantity - 1)">−</button>
                  <span>{{ item.quantity }}</span>
                  <button @click="cartStore.updateQty(item._key, item.quantity + 1)">+</button>
                </div>
              </div>
              <div class="ci-right">
                <p class="ci-price">{{ fmt(item.price * item.quantity) }}</p>
                <button class="ci-remove" @click="cartStore.removeItem(item._key)" aria-label="Xoá">✕</button>
              </div>
            </div>
          </div>
        </div>

        <div class="cart-footer">
          <div v-if="cartStore.count > 0" class="cart-total-row">
            <span class="cart-total-label">Tổng cộng</span>
            <span class="cart-total-val">{{ fmt(cartStore.total) }}</span>
          </div>
          <RouterLink
            v-if="cartStore.count > 0"
            to="/thanh-toan"
            class="checkout-btn"
            @click="$emit('close')"
          >THANH TOÁN</RouterLink>
          <p class="cart-shipping-note">Miễn phí vận chuyển cho đơn từ 5.000.000 đ</p>
          <p class="cart-footer-label">Chấp Nhận Thanh Toán</p>
          <div class="payment-icons">
            <span v-for="p in ['PayPal','Visa','MasterCard','iDeal']" :key="p" class="pay-badge">{{ p }}</span>
          </div>
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
const cartStore = useCartStore()
defineProps({ open: { type: Boolean, default: false } })
defineEmits(['close'])
function fmt(n) { return Number(n).toLocaleString('vi-VN') + ' đ' }
function swatchGrad(hex) {
  if (!hex) return 'linear-gradient(160deg,#ece5d5,#d4c8b0)'
  return `linear-gradient(160deg,${hex}22,${hex}55)`
}
</script>

<style scoped>
.cart-overlay {
  position: fixed; inset: 0;
  background: rgba(26,26,24,.4);
  z-index: 1100;
  backdrop-filter: blur(2px);
}
.cart-drawer {
  position: fixed; top: 0; right: 0; bottom: 0;
  width: 420px; max-width: 100vw;
  background: var(--warm-white);
  z-index: 1101;
  display: flex; flex-direction: column;
  box-shadow: -8px 0 48px rgba(0,0,0,.15);
}
.cart-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 28px 28px 20px;
  border-bottom: 1px solid var(--border);
}
.cart-title { font-family: var(--font-display); font-size: 22px; font-weight: 400; }
.cart-count { color: var(--text-muted); font-size: 16px; }
.cart-close {
  background: none; border: none; color: var(--charcoal);
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  transition: color var(--transition); cursor: pointer;
}
.cart-close:hover { color: var(--gold); }
.cart-close svg { width: 20px; height: 20px; }
.cart-body { flex: 1; overflow-y: auto; padding: 20px 28px; }
.cart-empty {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; height: 100%; gap: 16px; text-align: center; padding: 40px 0;
}
.cart-empty-icon svg { width: 56px; height: 56px; color: var(--border); }
.cart-empty-text { font-size: 13px; color: var(--text-muted); }
.cart-shop-link {
  font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  color: var(--charcoal); border-bottom: 1px solid var(--charcoal);
  padding-bottom: 2px; transition: color var(--transition), border-color var(--transition);
}
.cart-shop-link:hover { color: var(--gold); border-color: var(--gold); }
/* Items */
.cart-items { display: flex; flex-direction: column; gap: 20px; }
.cart-item { display: flex; gap: 12px; align-items: flex-start; }
.ci-img { width: 64px; height: 80px; flex-shrink: 0; border: 1px solid var(--border); }
.ci-info { flex: 1; }
.ci-name { font-size: 13px; font-weight: 500; line-height: 1.4; margin-bottom: 4px; text-transform: uppercase; }
.ci-meta { font-size: 11px; color: var(--text-muted); margin-bottom: 8px; }
.ci-qty { display: flex; align-items: center; gap: 8px; }
.ci-qty button {
  width: 24px; height: 24px; border: 1px solid var(--border);
  background: none; font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--transition);
}
.ci-qty button:hover { border-color: var(--charcoal); background: var(--charcoal); color: var(--cream); }
.ci-qty span { font-size: 13px; min-width: 20px; text-align: center; }
.ci-right { display: flex; flex-direction: column; align-items: flex-end; gap: 8px; flex-shrink: 0; }
.ci-price { font-size: 13px; font-weight: 500; white-space: nowrap; }
.ci-remove {
  background: none; border: none; font-size: 11px;
  color: var(--text-muted); cursor: pointer; transition: color var(--transition);
}
.ci-remove:hover { color: #c0395a; }
/* Footer */
.cart-footer { padding: 20px 28px 28px; border-top: 1px solid var(--border); }
.cart-total-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
}
.cart-total-label { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--text-muted); }
.cart-total-val { font-size: 18px; font-weight: 500; }
.checkout-btn {
  display: block; width: 100%; padding: 15px;
  background: var(--charcoal); color: var(--cream); text-align: center;
  font-size: 10px; letter-spacing: 4px; text-transform: uppercase; font-weight: 600;
  transition: opacity var(--transition); margin-bottom: 12px;
}
.checkout-btn:hover { opacity: .85; }
.cart-shipping-note {
  font-size: 10px; color: var(--text-muted); text-align: center;
  letter-spacing: .5px; margin-bottom: 16px;
}
.cart-footer-label { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; }
.payment-icons { display: flex; gap: 6px; flex-wrap: wrap; }
.pay-badge {
  font-size: 9px; letter-spacing: 1px; text-transform: uppercase;
  border: 1px solid var(--border); padding: 3px 8px;
  color: var(--text-muted); border-radius: 2px;
}
/* Transitions */
.overlay-enter-active, .overlay-leave-active { transition: opacity .3s; }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }
.drawer-enter-active, .drawer-leave-active { transition: transform .35s cubic-bezier(.25,.46,.45,.94); }
.drawer-enter-from, .drawer-leave-to { transform: translateX(100%); }
</style>
