<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Người dùng</div>
        <div class="page-sub">{{ total }} tài khoản</div>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="card toolbar">
      <input v-model="search" type="text" class="form-input" placeholder="Tìm email, tên..." style="max-width:280px" @keyup.enter="doSearch" />
      <select v-model="filterRole" class="form-select" style="max-width:160px" @change="doSearch">
        <option value="">Tất cả</option>
        <option value="admin">Admin</option>
        <option value="user">Người dùng</option>
      </select>
      <button class="btn btn-secondary" @click="doSearch">Tìm kiếm</button>
      <span style="font-size:13px;color:var(--text-2);margin-left:auto">{{ total }} kết quả</span>
    </div>

    <div class="card" style="margin-top:16px">
      <div v-if="loading" class="empty-state">Đang tải...</div>
      <div v-else-if="!users.length" class="empty-state">Không có người dùng nào</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Tên</th>
              <th>Email</th>
              <th>SĐT</th>
              <th>Vai trò</th>
              <th>Ngày đăng ký</th>
              <th style="width:120px">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>
                <div style="font-weight:500">{{ u.full_name || u.name || '—' }}</div>
              </td>
              <td>{{ u.email }}</td>
              <td>{{ u.phone || '—' }}</td>
              <td>
                <span class="badge" :class="u.is_admin ? 'badge-confirmed' : 'badge-refunded'">
                  {{ u.is_admin ? 'Admin' : 'Người dùng' }}
                </span>
              </td>
              <td>{{ formatDate(u.created_at) }}</td>
              <td>
                <div style="display:flex;gap:6px">
                  <button class="btn btn-secondary btn-sm" @click="openEdit(u)">Sửa</button>
                  <button class="btn btn-danger btn-sm" @click="confirmDelete(u)">Xoá</button>
                </div>
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

    <!-- Edit modal -->
    <div v-if="editModal.open" class="modal-overlay" @click.self="editModal.open=false">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">Sửa người dùng</div>
          <button class="modal-close" @click="editModal.open=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Họ tên</label>
            <input v-model="editForm.full_name" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="editForm.email" class="form-input" type="email" />
          </div>
          <div class="form-group">
            <label class="form-label">SĐT</label>
            <input v-model="editForm.phone" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Mật khẩu mới <span style="color:var(--text-2);font-weight:400">(để trống nếu không đổi)</span></label>
            <input v-model="editForm.password" class="form-input" type="password" placeholder="••••••••" />
          </div>
          <div class="form-group">
            <label style="display:flex;align-items:center;gap:10px;cursor:pointer">
              <div class="toggle" :class="{active: editForm.is_admin}" @click="editForm.is_admin = !editForm.is_admin">
                <div class="toggle-knob" />
              </div>
              <span class="form-label" style="margin:0">Quyền Admin</span>
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="editModal.open=false">Huỷ</button>
          <button class="btn btn-primary" @click="saveUser" :disabled="editModal.saving">
            {{ editModal.saving ? 'Đang lưu...' : 'Lưu' }}
          </button>
        </div>
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
          <p>Bạn có chắc muốn xoá tài khoản <strong>{{ deleteTarget.email }}</strong>?</p>
          <p style="margin-top:8px;color:var(--text-2);font-size:13px">Hành động này không thể hoàn tác.</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="deleteTarget=null">Huỷ</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? 'Đang xoá...' : 'Xoá tài khoản' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { usersApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'

const toast = useToastStore()

const users   = ref([])
const total   = ref(0)
const loading = ref(true)
const page    = ref(1)
const PER_PAGE = 20

const search     = ref('')
const filterRole = ref('')
const deleteTarget = ref(null)
const deleting   = ref(false)

const editModal = reactive({ open: false, target: null, saving: false })
const editForm  = reactive({ full_name: '', email: '', phone: '', password: '', is_admin: false })

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
    if (filterRole.value === 'admin') params.is_admin = true
    if (filterRole.value === 'user') params.is_admin = false
    const res = await usersApi.list(params)
    users.value = res.results ?? res
    total.value = res.total ?? res.length
  } catch (e) {
    console.error('[UsersView] load error:', e)
    users.value = []
  }
  finally { loading.value = false }
}

function doSearch() { page.value = 1; load() }
function goPage(p)  { page.value = p; load() }

function openEdit(u) {
  editModal.target = u
  editForm.full_name = u.full_name || u.name || ''
  editForm.email = u.email || ''
  editForm.phone = u.phone || ''
  editForm.password = ''
  editForm.is_admin = !!u.is_admin
  editModal.open = true
}

async function saveUser() {
  editModal.saving = true
  try {
    const payload = {
      full_name: editForm.full_name,
      email: editForm.email,
      phone: editForm.phone,
      is_admin: editForm.is_admin,
    }
    if (editForm.password) payload.password = editForm.password
    await usersApi.update(editModal.target.id, payload)
    toast.success('Cập nhật thành công')
    editModal.open = false
    load()
  } catch (e) { toast.error(String(e)) }
  finally { editModal.saving = false }
}

function confirmDelete(u) { deleteTarget.value = u }

async function doDelete() {
  deleting.value = true
  try {
    await usersApi.remove(deleteTarget.value.id)
    toast.success('Đã xoá tài khoản')
    deleteTarget.value = null
    load()
  } catch (e) { toast.error(String(e)) }
  finally { deleting.value = false }
}

function formatDate(d) { return d ? new Date(d).toLocaleDateString('vi-VN') : '—' }

onMounted(load)
</script>

<style scoped>
.toolbar { display: flex; align-items: center; gap: 10px; padding: 12px 16px; flex-wrap: wrap; }

.toggle {
  width: 36px; height: 20px;
  border-radius: 10px;
  background: #D1D5DB;
  position: relative;
  cursor: pointer;
  transition: background .2s;
  flex-shrink: 0;
}
.toggle.active { background: var(--brand); }
.toggle-knob {
  position: absolute;
  top: 2px; left: 2px;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: #fff;
  transition: left .2s;
  box-shadow: 0 1px 3px rgba(0,0,0,.2);
}
.toggle.active .toggle-knob { left: 18px; }
</style>
