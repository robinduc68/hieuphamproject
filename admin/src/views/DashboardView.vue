<template>
  <div>
    <!-- Stat cards -->
    <div class="stats-grid">
      <div class="stat-card card" v-for="s in stats" :key="s.label">
        <div class="stat-icon" :style="{ background: s.bg }">
          <span v-html="s.icon" />
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <!-- Recent orders -->
    <div class="card" style="margin-top:24px">
      <div class="card-head">
        <div class="card-title">Đơn hàng gần đây</div>
        <RouterLink to="/orders" class="btn btn-secondary btn-sm">Xem tất cả</RouterLink>
      </div>

      <div v-if="loadingOrders" class="empty-state">Đang tải...</div>
      <div v-else-if="!recentOrders.length" class="empty-state">Chưa có đơn hàng nào</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#ID</th>
              <th>Khách hàng</th>
              <th>SĐT</th>
              <th>Tổng tiền</th>
              <th>Trạng thái</th>
              <th>Ngày tạo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="o in recentOrders" :key="o.id" @click="$router.push('/orders')" style="cursor:pointer">
              <td><strong>#{{ o.id }}</strong></td>
              <td>{{ o.full_name || o.guest_name || '—' }}</td>
              <td>{{ o.phone || o.guest_phone || '—' }}</td>
              <td>{{ formatMoney(o.total || o.total_amount) }}</td>
              <td><span class="badge" :class="`badge-${o.status}`">{{ statusLabel(o.status) }}</span></td>
              <td>{{ formatDate(o.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statsApi, ordersApi } from '@/api/index.js'

const loadingOrders = ref(true)
const recentOrders  = ref([])

const statsData = ref({ total_orders: 0, total_revenue: 0, total_products: 0, total_users: 0 })

const stats = ref([
  { label: 'Tổng đơn hàng',  value: '—', bg: '#EDE9FE', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="#7C3AED" stroke-width="1.6"><path d="M4 4h12a1 1 0 011 1v10a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1z"/><path d="M7 8h6M7 11h4"/></svg>' },
  { label: 'Doanh thu',       value: '—', bg: '#D1FAE5', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="#059669" stroke-width="1.6"><path d="M10 2v16M6 6h6a2 2 0 010 4H8a2 2 0 000 4h7"/></svg>' },
  { label: 'Sản phẩm',        value: '—', bg: '#DBEAFE', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="#2563EB" stroke-width="1.6"><path d="M3 3h14l-1.5 9H4.5L3 3z"/><circle cx="8" cy="17" r="1"/><circle cx="14" cy="17" r="1"/></svg>' },
  { label: 'Người dùng',      value: '—', bg: '#FEF3C7', icon: '<svg viewBox="0 0 20 20" fill="none" stroke="#D97706" stroke-width="1.6"><circle cx="10" cy="7" r="3"/><path d="M3 17a7 7 0 0114 0"/></svg>' },
])

onMounted(async () => {
  // Load stats
  try {
    const s = await statsApi.get()
    stats.value[0].value = s.total_orders
    stats.value[1].value = formatMoney(s.total_revenue)
    stats.value[2].value = s.total_products
    stats.value[3].value = s.total_users
  } catch (e) {
    console.error('[DashboardView] stats error:', e)
  }

  // Load recent orders
  try {
    const res = await ordersApi.list({ page: 1, per_page: 8 })
    recentOrders.value = res.results ?? res
  } catch (e) {
    console.error('[DashboardView] orders error:', e)
    recentOrders.value = []
  } finally {
    loadingOrders.value = false
  }
})

function formatMoney(v) {
  if (!v) return '0 đ'
  return Number(v).toLocaleString('vi-VN') + ' đ'
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('vi-VN')
}

const STATUS_MAP = {
  pending: 'Chờ xác nhận', confirmed: 'Đã xác nhận',
  processing: 'Đang xử lý', shipped: 'Đang giao',
  delivered: 'Đã giao', cancelled: 'Đã huỷ', refunded: 'Hoàn tiền',
}
function statusLabel(s) { return STATUS_MAP[s] || s }
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.stat-icon :deep(svg) { width: 22px; height: 22px; }
.stat-value { font-size: 22px; font-weight: 700; line-height: 1.2; }
.stat-label { font-size: 12px; color: var(--text-2); margin-top: 2px; }

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}
.card-title { font-size: 15px; font-weight: 600; }

@media (max-width: 900px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 560px) {
  .stats-grid { grid-template-columns: 1fr; gap: 12px; }
}
</style>
