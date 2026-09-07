<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Tùy chỉnh sản phẩm</h1>
      <button v-if="auth.can('customization.update')" class="btn btn-primary" @click="openCreate">+ Thêm option</button>
    </div>

    <div v-if="loading" class="loading">Đang tải...</div>
    <div v-else-if="error" class="error-box">{{ error }}</div>

    <template v-else>
      <div v-for="group in groups" :key="group.group_key" class="group-card">
        <h2 class="group-title">{{ group.group_label }} <span class="group-key">({{ group.group_key }})</span></h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Option Key</th>
              <th>Tên hiển thị</th>
              <th>Phí thêm (VND)</th>
              <th>Sort</th>
              <th>Active</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="opt in group.options" :key="opt.id">
              <td><code>{{ opt.option_key }}</code></td>
              <td>{{ opt.option_label }}</td>
              <td class="price-cell">{{ formatPrice(opt.price_adjustment) }}</td>
              <td>{{ opt.sort_order }}</td>
              <td>
                <span :class="['badge', opt.is_active ? 'badge-green' : 'badge-gray']">
                  {{ opt.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <button v-if="auth.can('customization.update')" class="btn btn-sm btn-secondary" @click="openEdit(opt)">Sửa</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- Edit/Create modal -->
    <Teleport to="body">
      <Transition name="overlay">
        <div v-if="modal.open" class="modal-overlay" @click="closeModal" />
      </Transition>
      <Transition name="modal">
        <div v-if="modal.open" class="modal" role="dialog" aria-modal="true">
          <div class="modal-header">
            <h3>{{ modal.isCreate ? 'Thêm option' : 'Chỉnh sửa option' }}</h3>
            <button class="modal-close" @click="closeModal">✕</button>
          </div>
          <div class="modal-body">
            <div class="form-grid">
              <template v-if="modal.isCreate">
                <label class="form-label">Group Key</label>
                <input v-model="modal.form.group_key" class="form-input" placeholder="vd: tailoring_method" />
                <label class="form-label">Group Label</label>
                <input v-model="modal.form.group_label" class="form-input" placeholder="vd: Hình thức may" />
                <label class="form-label">Option Key</label>
                <input v-model="modal.form.option_key" class="form-input" placeholder="vd: custom" />
                <label class="form-label">Option Label</label>
                <input v-model="modal.form.option_label" class="form-input" placeholder="vd: May theo số đo" />
              </template>
              <template v-else>
                <label class="form-label">Group Label</label>
                <input v-model="modal.form.group_label" class="form-input" />
                <label class="form-label">Option Label</label>
                <input v-model="modal.form.option_label" class="form-input" />
              </template>

              <label class="form-label">Phí thêm (VND)</label>
              <input v-model.number="modal.form.price_adjustment" type="number" min="0" step="1000" class="form-input" />

              <label class="form-label">Sort order</label>
              <input v-model.number="modal.form.sort_order" type="number" min="0" class="form-input" />

              <template v-if="!modal.isCreate">
                <label class="form-label">Active</label>
                <select v-model="modal.form.is_active" class="form-input">
                  <option :value="true">Active</option>
                  <option :value="false">Inactive</option>
                </select>
              </template>
            </div>

            <div v-if="modal.error" class="error-box mt-8">{{ modal.error }}</div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Huỷ</button>
            <button class="btn btn-primary" :disabled="modal.saving" @click="saveModal">
              {{ modal.saving ? 'Đang lưu...' : 'Lưu' }}
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { customizationApi } from '@/api/index.js'
import { useAuthStore } from '@/stores/auth.js'

const auth    = useAuthStore()

const groups  = ref([])
const loading = ref(true)
const error   = ref('')

const modal = ref({
  open: false, isCreate: false, saving: false, error: '',
  id: null,
  form: { group_key: '', group_label: '', option_key: '', option_label: '', price_adjustment: 0, sort_order: 0, is_active: true },
})

async function fetchAll() {
  loading.value = true
  error.value   = ''
  try {
    const all = await customizationApi.listAll()  // interceptor đã unwrap, không cần .data
    const map = {}
    for (const opt of all) {
      if (!map[opt.group_key]) {
        map[opt.group_key] = { group_key: opt.group_key, group_label: opt.group_label, options: [] }
      }
      map[opt.group_key].options.push(opt)
    }
    groups.value = Object.values(map)
  } catch (e) {
    error.value = String(e) || 'Không thể tải dữ liệu.'
    console.error('[CustomizationView] fetchAll error:', e)
  } finally {
    loading.value = false
  }
}

function openCreate() {
  modal.value = {
    open: true, isCreate: true, saving: false, error: '',
    id: null,
    form: { group_key: '', group_label: '', option_key: '', option_label: '', price_adjustment: 0, sort_order: 0, is_active: true },
  }
}

function openEdit(opt) {
  modal.value = {
    open: true, isCreate: false, saving: false, error: '',
    id: opt.id,
    form: {
      group_key:        opt.group_key,
      group_label:      opt.group_label,
      option_key:       opt.option_key,
      option_label:     opt.option_label,
      price_adjustment: Number(opt.price_adjustment),
      sort_order:       opt.sort_order,
      is_active:        opt.is_active,
    },
  }
}

function closeModal() {
  modal.value.open = false
}

async function saveModal() {
  modal.value.saving = true
  modal.value.error  = ''
  try {
    if (modal.value.isCreate) {
      await customizationApi.create(modal.value.form)
    } else {
      const { group_key, option_key, ...patch } = modal.value.form
      await customizationApi.update(modal.value.id, patch)
    }
    closeModal()
    await fetchAll()
  } catch (e) {
    modal.value.error = String(e) || 'Có lỗi xảy ra.'
  } finally {
    modal.value.saving = false
  }
}

function formatPrice(n) {
  if (!n || n == 0) return 'Miễn phí'
  return '+' + Number(n).toLocaleString('vi-VN') + ' đ'
}

onMounted(fetchAll)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}
.page-title { font-size: 20px; font-weight: 600; }

.group-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.group-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 14px;
  color: var(--text);
}
.group-key {
  font-size: 12px;
  font-weight: 400;
  color: var(--text-muted);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.data-table th {
  text-align: left;
  padding: 8px 12px;
  border-bottom: 2px solid var(--border);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.data-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: var(--bg); }

.price-cell { font-weight: 600; color: var(--brand); }

code {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-family: monospace;
}

.badge { padding: 3px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-green { background: #dcfce7; color: #166534; }
.badge-gray  { background: #f3f4f6; color: #6b7280; }

.loading  { text-align: center; padding: 40px; color: var(--text-muted); }
.error-box { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; }
.mt-8 { margin-top: 8px; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.4);
  z-index: 1000;
}
.modal {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 480px;
  max-width: calc(100vw - 32px);
  background: #fff;
  border-radius: 12px;
  z-index: 1001;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--border);
}
.modal-header h3 { font-size: 16px; font-weight: 600; }
.modal-close { background: none; border: none; font-size: 18px; cursor: pointer; color: #999; }
.modal-body { padding: 20px 24px; }
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  border-top: 1px solid var(--border);
}

.form-grid { display: flex; flex-direction: column; gap: 10px; }
.form-label { font-size: 12px; font-weight: 600; color: var(--text-muted); }
.form-input {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  box-sizing: border-box;
}
.form-input:focus { border-color: var(--brand); }

.overlay-enter-active, .overlay-leave-active { transition: opacity .2s; }
.overlay-enter-from,   .overlay-leave-to     { opacity: 0; }
.modal-enter-active, .modal-leave-active {
  transition: opacity .2s ease, transform .2s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: translate(-50%, -48%);
}
</style>
