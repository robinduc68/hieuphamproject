<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Đơn hàng</div>
        <div class="page-sub">{{ total }} đơn hàng</div>
      </div>
    </div>

    <!-- Filter -->
    <div class="card toolbar">
      <select v-model="filterStatus" class="form-select" style="max-width:180px" @change="load">
        <option value="">Tất cả trạng thái</option>
        <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
      </select>
      <span style="font-size:13px;color:var(--text-2);margin-left:auto">{{ total }} kết quả</span>
    </div>

    <div class="card" style="margin-top:16px">
      <div v-if="loading" class="empty-state">Đang tải...</div>
      <div v-else-if="!orders.length" class="empty-state">Không có đơn hàng nào</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Khách hàng</th>
              <th>SĐT</th>
              <th>Địa chỉ</th>
              <th>Tổng tiền</th>
              <th>Trạng thái</th>
              <th>Ngày tạo</th>
              <th style="width:100px">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="o in orders" :key="o.id">
              <td><strong>#{{ o.id }}</strong></td>
              <td>{{ o.full_name || o.guest_name || '—' }}</td>
              <td>{{ o.phone || o.guest_phone || '—' }}</td>
              <td style="max-width:200px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ o.address || o.shipping_address || '—' }}</td>
              <td><strong>{{ formatMoney(o.grand_total || o.total) }}</strong></td>
              <td>
                <span class="badge" :class="`badge-${o.status}`">{{ statusLabel(o.status) }}</span>
                <span class="badge badge-pay" :class="o.payment_status === 'paid' ? 'badge-green' : 'badge-orange'" style="margin-left:4px">{{ o.payment_status === 'paid' ? 'Đã TT' : 'Chưa TT' }}</span>
              </td>
              <td>{{ formatDate(o.created_at) }}</td>
              <td>
                <button class="btn btn-secondary btn-sm" @click="openDetail(o)">Chi tiết</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button class="pg-btn" :disabled="page===1" @click="goPage(page-1)">←</button>
        <button v-for="n in pageNums" :key="n" class="pg-btn" :class="{active:n===page}" @click="goPage(n)">{{ n }}</button>
        <button class="pg-btn" :disabled="page===totalPages" @click="goPage(page+1)">→</button>
      </div>
    </div>

    <!-- Order detail modal -->
    <div v-if="selected" class="modal-overlay" @click.self="selected=null">
      <div class="modal modal-lg">
        <div class="modal-header">
          <div class="modal-title">Đơn hàng #{{ selected.id }}</div>
          <button class="modal-close" @click="selected=null">✕</button>
        </div>
        <div class="modal-body">
          <div class="order-info-grid">
            <div><span class="info-label">Khách hàng</span><span>{{ selected.full_name || selected.guest_name }}</span></div>
            <div><span class="info-label">SĐT</span><span>{{ selected.phone || selected.guest_phone }}</span></div>
            <div><span class="info-label">Email</span><span>{{ selected.email || selected.guest_email }}</span></div>
            <div><span class="info-label">Địa chỉ</span><span>{{ selected.address || selected.shipping_address }}</span></div>
            <div><span class="info-label">Ghi chú</span><span>{{ selected.note || '—' }}</span></div>
            <div><span class="info-label">Mã vận đơn</span><span>{{ selected.tracking_code || '—' }}</span></div>
            <div><span class="info-label">TT thanh toán</span><span>{{ selected.payment_status === 'paid' ? 'Đã thanh toán' : 'Chưa thanh toán' }}</span></div>
            <div><span class="info-label">Hình thức TT</span><span>{{ selected.payment_method || '—' }}</span></div>
          </div>

          <div style="margin-top:20px;margin-bottom:12px;font-weight:600">Sản phẩm</div>
          <table>
            <thead><tr><th>Sản phẩm</th><th>Size</th><th>SL</th><th>Đơn giá</th><th>Thành tiền</th></tr></thead>
            <tbody>
              <tr v-for="item in selected.items" :key="item.id">
                <td>{{ item.product_name || item.product_id }}</td>
                <td>{{ item.size_label || item.size }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ formatMoney(item.unit_price || item.price) }}</td>
                <td>{{ formatMoney((item.unit_price || item.price) * item.quantity) }}</td>
              </tr>
            </tbody>
          </table>

          <div style="text-align:right;margin-top:12px">
            <div style="font-size:13px;color:var(--text-2)">Tạm tính: {{ formatMoney(selected.total) }}</div>
            <div v-if="selected.discount_amount > 0" style="font-size:13px;color:#16a34a">Giảm giá: -{{ formatMoney(selected.discount_amount) }}</div>
            <div style="font-size:15px;font-weight:700;margin-top:4px">Tổng: {{ formatMoney(selected.grand_total || selected.total) }}</div>
          </div>

          <!-- Update status -->
          <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--border)">
            <div style="font-weight:600;margin-bottom:12px">Cập nhật trạng thái</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end">
              <div class="form-group" style="margin:0;flex:1">
                <label class="form-label">Trạng thái đơn</label>
                <select v-model="newStatus" class="form-select">
                  <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </div>
              <div class="form-group" style="margin:0;flex:1">
                <label class="form-label">Thanh toán</label>
                <select v-model="newPayStatus" class="form-select">
                  <option value="unpaid">Chưa thanh toán</option>
                  <option value="paid">Đã thanh toán</option>
                  <option value="refunded">Đã hoàn tiền</option>
                </select>
              </div>
              <div class="form-group" style="margin:0;flex:1">
                <label class="form-label">Mã vận đơn</label>
                <input v-model="trackingCode" class="form-input" placeholder="VTL123456..." />
              </div>
              <button v-if="auth.can('orders.update_status')" class="btn btn-primary" @click="updateStatus" :disabled="updatingStatus">
                {{ updatingStatus ? 'Đang cập nhật...' : 'Lưu' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ordersApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import { useAuthStore } from '@/stores/auth.js'

const toast = useToastStore()
const auth = useAuthStore()

const orders       = ref([])
const total        = ref(0)
const loading      = ref(true)
const page         = ref(1)
const PER_PAGE     = 20
const filterStatus = ref('')
const selected     = ref(null)
const newStatus      = ref('')
const newPayStatus   = ref('')
const trackingCode   = ref('')
const updatingStatus = ref(false)

const statusOptions = [
  { value: 'pending',    label: 'Chờ xác nhận' },
  { value: 'confirmed',  label: 'Đã xác nhận' },
  { value: 'processing', label: 'Đang xử lý' },
  { value: 'shipped',    label: 'Đang giao' },
  { value: 'delivered',  label: 'Đã giao' },
  { value: 'cancelled',  label: 'Đã huỷ' },
  { value: 'refunded',   label: 'Hoàn tiền' },
]

const STATUS_MAP = Object.fromEntries(statusOptions.map(s => [s.value, s.label]))
function statusLabel(s) { return STATUS_MAP[s] || s }

const totalPages = computed(() => Math.ceil(total.value / PER_PAGE))
const pageNums   = computed(() => {
  const nums = [], c = page.value, l = totalPages.value
  for (let i = Math.max(1, c-2); i <= Math.min(l, c+2); i++) nums.push(i)
  return nums
})

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, per_page: PER_PAGE }
    if (filterStatus.value) params.status = filterStatus.value
    const res = await ordersApi.list(params)
    orders.value = res.results ?? res
    total.value  = res.total  ?? res.length
  } catch (e) {
    console.error('[OrdersView] load error:', e)
    orders.value = []
  }
  finally { loading.value = false }
}

function goPage(p) { page.value = p; load() }

function openDetail(o) {
  selected.value      = o
  newStatus.value     = o.status
  newPayStatus.value  = o.payment_status || 'unpaid'
  trackingCode.value  = o.tracking_code || ''
}

async function updateStatus() {
  updatingStatus.value = true
  try {
    const updated = await ordersApi.updateStatus(selected.value.id, {
      status:         newStatus.value,
      payment_status: newPayStatus.value || undefined,
      tracking_code:  trackingCode.value || undefined,
    })
    const idx = orders.value.findIndex(o => o.id === selected.value.id)
    if (idx !== -1) orders.value[idx] = { ...orders.value[idx], ...updated }
    selected.value = { ...selected.value, status: newStatus.value, tracking_code: trackingCode.value }
    toast.success('Cập nhật trạng thái thành công')
  } catch (e) { toast.error(String(e)) }
  finally { updatingStatus.value = false }
}

function formatMoney(v) { return Number(v || 0).toLocaleString('vi-VN') + ' đ' }
function formatDate(d)  { return d ? new Date(d).toLocaleDateString('vi-VN') : '—' }

onMounted(load)
</script>

<style scoped>
.toolbar { display: flex; align-items: center; gap: 10px; padding: 12px 16px; }
.order-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.order-info-grid > div { display: flex; flex-direction: column; gap: 2px; }
.info-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; color: var(--text-2); }
.badge-green  { background: #dcfce7 !important; color: #166534 !important; }
.badge-orange { background: #fff7ed !important; color: #c2410c !important; }
</style>
