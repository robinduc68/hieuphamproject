<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Tin tức</div>
        <div class="page-sub">{{ total }} bài viết</div>
      </div>
      <RouterLink to="/posts/new" class="btn btn-primary">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M8 2v12M2 8h12"/></svg>
        Viết bài mới
      </RouterLink>
    </div>

    <!-- Toolbar -->
    <div class="card toolbar">
      <input v-model="search" type="text" class="form-input" placeholder="Tìm theo tiêu đề..." style="max-width:280px" @keyup.enter="doSearch" />
      <button class="btn btn-secondary" @click="doSearch">Tìm kiếm</button>
    </div>

    <!-- Table -->
    <div class="card" style="margin-top:16px">
      <div v-if="loading" class="empty-state">Đang tải...</div>
      <div v-else-if="!posts.length" class="empty-state">Chưa có bài viết nào</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th style="width:70px">Ảnh bìa</th>
              <th>Tiêu đề</th>
              <th style="width:140px">Nhãn</th>
              <th style="width:110px">Ngày đăng</th>
              <th style="width:110px">Trạng thái</th>
              <th style="width:120px">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in posts" :key="p.id">
              <td>
                <div class="post-thumb" :style="{ background: p.cover_color || '#E5E7EB' }">
                  <img v-if="p.cover_image" :src="p.cover_image" :alt="p.title" />
                </div>
              </td>
              <td>
                <div class="post-title-cell">{{ p.title }}</div>
                <div style="font-size:11px;color:var(--text-2)">{{ p.slug }}</div>
              </td>
              <td>{{ p.tag || '—' }}</td>
              <td>{{ formatDate(p.published_at) }}</td>
              <td>
                <span v-if="p.is_published" class="badge badge-confirmed">Đang đăng</span>
                <span v-else class="badge badge-refunded">Bản nháp</span>
              </td>
              <td>
                <div style="display:flex;gap:6px">
                  <RouterLink :to="`/posts/${p.id}/edit`" class="btn btn-icon btn-sm" title="Sửa">
                    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" style="width:13px;height:13px"><path d="M11 2l3 3L5 14H2v-3L11 2z"/></svg>
                  </RouterLink>
                  <button class="btn btn-icon btn-sm" title="Xoá" @click="deleteTarget = p">
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
          <p>Bạn có chắc muốn xoá bài viết <strong>{{ deleteTarget.title }}</strong>?</p>
          <p style="margin-top:8px;color:var(--text-2);font-size:13px">
            Bài viết bị xoá hẳn khỏi database, không khôi phục được. Nếu chỉ muốn tạm ẩn,
            hãy mở bài viết và tắt “Đang đăng”.
          </p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="deleteTarget=null">Huỷ</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? 'Đang xoá...' : 'Xoá bài viết' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { postsApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'

const toast = useToastStore()

const posts   = ref([])
const total   = ref(0)
const loading = ref(true)
const page    = ref(1)
const PER_PAGE = 15

const search       = ref('')
const deleteTarget = ref(null)
const deleting     = ref(false)

const totalPages = computed(() => Math.ceil(total.value / PER_PAGE))
const pageNums   = computed(() => {
  const nums = [], c = page.value, l = totalPages.value
  for (let i = Math.max(1, c - 2); i <= Math.min(l, c + 2); i++) nums.push(i)
  return nums
})

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, per_page: PER_PAGE }
    if (search.value) params.search = search.value
    const res = await postsApi.list(params)
    posts.value = res.results ?? res
    total.value = res.total ?? res.length
  } catch (e) {
    console.error('[PostsView] load error:', e)
    posts.value = []
  } finally {
    loading.value = false
  }
}

function doSearch() { page.value = 1; load() }
function goPage(p)  { page.value = p; load() }

async function doDelete() {
  deleting.value = true
  try {
    await postsApi.remove(deleteTarget.value.id)
    toast.success(`Đã xoá "${deleteTarget.value.title}"`)
    deleteTarget.value = null
    load()
  } catch (e) {
    toast.error(String(e))
  } finally {
    deleting.value = false
  }
}

function formatDate(d) {
  if (!d) return '—'
  const [y, m, day] = String(d).slice(0, 10).split('-')
  return `${day}/${m}/${y}`
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  flex-wrap: wrap;
}
.post-thumb {
  width: 56px; height: 40px;
  border-radius: 6px;
  overflow: hidden;
}
.post-thumb img { width: 100%; height: 100%; object-fit: cover; }
.post-title-cell { font-weight: 500; max-width: 380px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>
