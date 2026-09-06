<template>
  <Teleport to="body">
    <Transition name="overlay">
      <div v-if="modelValue" class="modal-overlay" @click="close" />
    </Transition>
    <Transition name="modal">
      <div v-if="modelValue" class="modal" role="dialog" aria-modal="true" :aria-label="title">
        <div class="modal-header">
          <h3 class="modal-title">{{ title }}</h3>
          <button class="modal-close" @click="close" aria-label="Đóng">✕</button>
        </div>
        <div class="modal-body">
          <!-- Nội dung do admin soạn ở trang admin → Nội dung web -->
          <div v-if="html" class="rich-text" v-html="html" />

          <div v-else class="table-scroll">
            <table class="guide-table">
              <thead>
                <tr><th v-for="(col, i) in columns" :key="i">{{ col }}</th></tr>
              </thead>
              <tbody>
                <tr v-for="(row, ri) in rows" :key="ri">
                  <td v-for="(col, ci) in columns" :key="ci">{{ row[ci] }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p v-if="note" class="guide-note">{{ note }}</p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  modelValue: { type: Boolean, default: false },
  title:      { type: String,  default: '' },
  note:       { type: String,  default: '' },
  columns:    { type: Array,   default: () => [] },
  rows:       { type: Array,   default: () => [] },
  html:       { type: String,  default: '' },   // có html thì hiện nội dung soạn thảo thay cho bảng
})
const emit = defineEmits(['update:modelValue'])

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; z-index: 1200;
  background: rgba(26,26,24,.5); backdrop-filter: blur(2px);
}
.modal {
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 680px; max-width: calc(100vw - 32px); max-height: 80vh; overflow-y: auto;
  background: var(--warm-white); z-index: 1201;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 28px 32px 20px; border-bottom: 1px solid var(--border);
}
.modal-title {
  font-family: var(--font-display); font-size: 22px; font-weight: 400;
  letter-spacing: 1px; color: var(--charcoal);
}
.modal-close {
  background: none; border: none; font-size: 18px; line-height: 1;
  color: var(--text-muted); cursor: pointer; transition: color var(--transition);
}
.modal-close:hover { color: var(--charcoal); }
.modal-body { padding: 28px 32px; }

.table-scroll { overflow-x: auto; }
.guide-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.guide-table th, .guide-table td {
  text-align: center; padding: 10px 12px; border-bottom: 1px solid var(--border);
}
.guide-table th {
  font-family: var(--font-body); font-size: 9px; font-weight: 600;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--text-muted); background: var(--cream-dark);
}
.guide-table tr:hover td { background: var(--cream); }
.guide-note {
  margin-top: 16px; font-size: 11px; font-style: italic;
  line-height: 1.6; color: var(--text-muted);
}

.overlay-enter-active, .overlay-leave-active { transition: opacity .3s; }
.overlay-enter-from,   .overlay-leave-to     { opacity: 0; }
.modal-enter-active, .modal-leave-active { transition: opacity .3s ease, transform .3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: translate(-50%, -46%); }

@media (max-width: 640px) {
  .modal-header { padding: 22px 20px 16px; }
  .modal-body   { padding: 22px 20px; }
}
</style>
