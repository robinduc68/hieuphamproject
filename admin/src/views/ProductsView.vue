<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Sản phẩm</div>
        <div class="page-sub">{{ total }} sản phẩm</div>
      </div>
      <RouterLink to="/products/new" class="btn btn-primary">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M8 2v12M2 8h12"/></svg>
        Thêm sản phẩm
      </RouterLink>
    </div>

    <!-- Toolbar -->
    <div class="card toolbar">
      <input v-model="search" type="text" class="form-input" placeholder="Tìm tên sản phẩm..." style="max-width:280px" @keyup.enter="doSearch" />
      <select v-model="filterCategory" class="form-select" style="max-width:180px" @change="doSearch">
        <option value="">Tất cả danh mục</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
      <select v-model="filterStatus" class="form-select" style="max-width:160px" @change="doSearch">
        <option value="">Tất cả</option>
        <option value="new">Mới</option>
        <option value="featured">Nổi bật</option>
      </select>
      <button class="btn btn-secondary" @click="doSearch">Tìm kiếm</button>
    </div>

    <!-- Table -->
    <div class="card" style="margin-top:16px">
      <div v-if="loading" class="empty-state">Đang tải...</div>
      <div v-else-if="!products.length" class="empty-state">Không có sản phẩm nào</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th style="width:56px">Ảnh</th>
              <th>Tên sản phẩm</th>
              <th>Danh mục</th>
              <th>Giá</th>
              <th>Trạng thái</th>
              <th style="width:120px">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.id">
              <td>
                <div class="product-thumb">
                  <img v-if="p.images?.length" :src="p.images[0].url" :alt="p.name" />
                  <div v-else class="thumb-placeholder" />
                </div>
              </td>
              <td>
                <div class="product-name-cell">{{ p.name }}</div>
                <div style="font-size:11px;color:var(--text-2)">{{ p.slug }}</div>
              </td>
              <td>{{ p.category?.name || '—' }}</td>
              <td>{{ formatMoney(p.price) }}</td>
              <td>
                <span v-if="p.is_new" class="badge badge-confirmed" style="margin-right:4px">Mới</span>
                <span v-if="p.is_featured" class="badge badge-shipped">Nổi bật</span>
                <span v-if="!p.is_new && !p.is_featured" class="badge badge-refunded">Thường</span>
              </td>
              <td>
                <div style="display:flex;gap:6px">
                  <RouterLink :to="`/products/${p.id}/edit`" class="btn btn-icon btn-sm" title="Sửa">
                    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" style="width:13px;height:13px"><path d="M11 2l3 3L5 14H2v-3L11 2z"/></svg>
                  </RouterLink>
                  <button class="btn btn-icon btn-sm" title="Xoá" @click="confirmDelete(p)">
                    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" style="width:13px;height:13px"><path d="M2 4h12M5 4V2h6v2M6 7v5M10 7v5M3 4l1 10h8l1-10"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button class="pg-btn" :disabled="page===1" @click="goPage(page-1)">←</button>
        <button v-for="n in pageNums" :key="n" class="pg-btn" :class="{active:n===page}" @click="goPage(n)">{{ n }}</button>
        <button class="pg-btn" :disabled="page===totalPages" @click="goPage(page+1)">→</button>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget=null">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">Xác nhận xoá</div>
          <button class="modal-close" @click="deleteTarget=null">✕</button>
        </div>
        <div class="modal-body">
          <p>Bạn có chắc muốn xoá sản phẩm <strong>{{ deleteTarget.name }}</strong>?</p>
          <p style="margin-top:8px;color:var(--text-2);font-size:13px">Sản phẩm sẽ bị ẩn khỏi cửa hàng (soft delete).</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="deleteTarget=null">Huỷ</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? 'Đang xoá...' : 'Xoá sản phẩm' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productsApi, categoriesApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'

const toast = useToastStore()

const products   = ref([])
const categories = ref([])
const total      = ref(0)
const loading    = ref(true)
const page       = ref(1)
const PER_PAGE   = 15

const search         = ref('')
const filterCategory = ref('')
const filterStatus   = ref('')
const deleteTarget   = ref(null)
const deleting       = ref(false)

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
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category_id = filterCategory.value
    if (filterStatus.value === 'new') params.is_new = true
    if (filterStatus.value === 'featured') params.is_featured = true
    const res = await productsApi.list(params)
    products.value = res.results ?? res
    total.value    = res.total ?? res.length
  } catch (e) {
    console.error('[ProductsView] load error:', e)
    products.value = []
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    categories.value = await categoriesApi.list()
  } catch (e) {
    console.error('[ProductsView] loadCategories error:', e)
    categories.value = []
  }
}

function doSearch() { page.value = 1; load() }
function goPage(p)  { page.value = p; load() }

function confirmDelete(p) { deleteTarget.value = p }

async function doDelete() {
  deleting.value = true
  try {
    await productsApi.remove(deleteTarget.value.id)
    toast.success(`Đã xoá "${deleteTarget.value.name}"`)
    deleteTarget.value = null
    load()
  } catch (e) {
    toast.error(String(e))
  } finally {
    deleting.value = false
  }
}

function formatMoney(v) {
  return Number(v || 0).toLocaleString('vi-VN') + ' đ'
}

onMounted(() => { load(); loadCategories() })
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  flex-wrap: wrap;
}
.product-thumb {
  width: 40px; height: 48px;
  border-radius: 6px;
  overflow: hidden;
  background: var(--bg);
}
.product-thumb img { width: 100%; height: 100%; object-fit: cover; }
.thumb-placeholder { width: 100%; height: 100%; background: #E5E7EB; }
.product-name-cell { font-weight: 500; max-width: 260px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>
