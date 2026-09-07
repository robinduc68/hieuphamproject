<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Người dùng</div>
        <div class="page-sub">{{ total }} tài khoản</div>
      </div>
      <button v-if="auth.can('users.create')" class="btn btn-primary" @click="openCreate">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M8 2v12M2 8h12"/></svg>
        Thêm tài khoản
      </button>
    </div>

    <!-- Toolbar -->
    <div class="card toolbar">
      <input v-model="search" type="text" class="form-input" placeholder="Tìm email, tên..." style="max-width:280px" @keyup.enter="doSearch" />
      <select v-model="filterRole" class="form-select" style="max-width:160px" @change="doSearch">
        <option value="">Tất cả tài khoản</option>
        <option value="admin">Admin</option>
        <option value="user">Khách</option>
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
              <th style="width:120px">Vai trò</th>
              <th style="width:130px">Trạng thái</th>
              <th style="width:110px">Ngày đăng ký</th>
              <th style="width:210px">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id" :class="{ 'row-locked': !u.is_active }">
              <td>{{ u.id }}</td>
              <td>
                <div style="font-weight:500">
                  {{ u.full_name || '—' }}
                  <span v-if="u.id === myId" class="self-tag">bạn</span>
                </div>
              </td>
              <td>{{ u.email }}</td>
              <td>{{ u.phone || '—' }}</td>
              <td>
                <span class="badge" :class="u.is_admin ? 'badge-confirmed' : 'badge-refunded'">
                  {{ u.is_admin ? (u.role_name || 'Admin (chưa có vai trò)') : 'Khách' }}
                </span>
              </td>
              <td>
                <span class="badge" :class="u.is_active ? 'badge-shipped' : 'badge-cancelled'">
                  {{ u.is_active ? 'Hoạt động' : 'Đã khoá' }}
                </span>
              </td>
              <td>{{ formatDate(u.created_at) }}</td>
              <td>
                <div style="display:flex;gap:6px;flex-wrap:wrap">
                  <button class="btn btn-secondary btn-sm" :disabled="!auth.can('users.update')" @click="openEdit(u)">Sửa</button>
                  <button
                    class="btn btn-secondary btn-sm"
                    :disabled="u.id === myId || busyId === u.id || !auth.can('users.update')"
                    :title="u.id === myId ? 'Không thể tự khoá tài khoản của mình' : ''"
                    @click="toggleActive(u)"
                  >{{ u.is_active ? 'Khoá' : 'Mở khoá' }}</button>
                  <button
                    class="btn btn-danger btn-sm"
                    :disabled="u.id === myId || !auth.can('users.delete')"
                    :title="u.id === myId ? 'Không thể xoá chính mình' : ''"
                    @click="deleteTarget = u"
                  >Xoá</button>
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

    <!-- Modal tạo / sửa -->
    <div v-if="formModal.open" class="modal-overlay" @click.self="formModal.open=false">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">{{ isCreate ? 'Thêm tài khoản' : 'Sửa tài khoản' }}</div>
          <button class="modal-close" @click="formModal.open=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Họ tên</label>
            <input v-model="form.full_name" class="form-input" placeholder="Nguyễn Văn A" />
          </div>
          <div class="form-group">
            <label class="form-label">Email *</label>
            <input v-model="form.email" class="form-input" type="email" placeholder="ten@email.com" />
          </div>
          <div class="form-group">
            <label class="form-label">SĐT</label>
            <input v-model="form.phone" class="form-input" placeholder="09xxxxxxxx" />
          </div>
          <div class="form-group">
            <label class="form-label">
              {{ isCreate ? 'Mật khẩu *' : 'Mật khẩu mới' }}
              <span v-if="!isCreate" style="color:var(--text-2);font-weight:400">(để trống nếu không đổi)</span>
            </label>
            <input v-model="form.password" class="form-input" type="password" placeholder="••••••••" />
            <span class="form-hint">Tối thiểu {{ MIN_PASSWORD_LEN }} ký tự.</span>
          </div>

          <div class="form-group">
            <label class="form-label">Loại tài khoản</label>
            <select v-model="form.is_admin" class="form-select" :disabled="isSelf">
              <option :value="false">Người dùng — chỉ mua hàng ngoài website</option>
              <option :value="true">Admin — vào được trang quản trị</option>
            </select>
            <span v-if="isSelf" class="form-hint">Không thể tự bỏ quyền admin của chính mình.</span>
            <span v-else class="form-hint">Tài khoản admin vào được trang quản trị; làm được gì thì tuỳ vai trò bên dưới.</span>
          </div>

          <div v-if="form.is_admin" class="form-group">
            <label class="form-label">Vai trò *</label>
            <select v-model="form.role_id" class="form-select" :disabled="isSelf">
              <option :value="null">— Chọn vai trò —</option>
              <option v-for="r in roles" :key="r.id" :value="r.id">{{ r.name }}</option>
            </select>
            <span class="form-hint">
              <template v-if="selectedRole?.description">{{ selectedRole.description }}</template>
              <template v-else>Quyết định tài khoản này vào được tab nào, bấm được nút nào.</template>
              <template v-if="canManageRoles">
                — sửa danh sách vai trò ở <RouterLink to="/roles">Vai trò & phân quyền</RouterLink>.
              </template>
            </span>
            <span v-if="isSelf" class="form-hint">Không thể tự đổi vai trò của chính mình.</span>
          </div>

          <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Trạng thái</label>
            <select v-model="form.is_active" class="form-select" :disabled="isSelf">
              <option :value="true">Hoạt động — đăng nhập bình thường</option>
              <option :value="false">Khoá — chặn đăng nhập, giữ nguyên dữ liệu</option>
            </select>
            <span v-if="isSelf" class="form-hint">Không thể tự khoá tài khoản của chính mình.</span>
          </div>

          <div v-if="formModal.error" class="error-box" style="margin-top:16px">{{ formModal.error }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="formModal.open=false">Huỷ</button>
          <button class="btn btn-primary" @click="submitForm" :disabled="formModal.saving">
            {{ formModal.saving ? 'Đang lưu...' : (isCreate ? 'Tạo tài khoản' : 'Lưu') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal xoá -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget=null">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">Xác nhận xoá</div>
          <button class="modal-close" @click="deleteTarget=null">✕</button>
        </div>
        <div class="modal-body">
          <p>Xoá vĩnh viễn tài khoản <strong>{{ deleteTarget.email }}</strong>?</p>
          <p style="margin-top:8px;color:var(--text-2);font-size:13px">
            Tài khoản bị xoá hẳn khỏi database, không khôi phục được. Đơn hàng cũ của người này
            vẫn giữ nguyên (đã lưu sẵn tên, email, địa chỉ lúc đặt) nhưng không còn gắn với tài khoản nào.
          </p>
          <p style="margin-top:8px;color:var(--text-2);font-size:13px">
            Chỉ muốn chặn đăng nhập mà vẫn giữ tài khoản thì bấm <strong>Khoá</strong> thay vì xoá.
          </p>
          <div v-if="deleteError" class="error-box" style="margin-top:14px">{{ deleteError }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="deleteTarget=null">Huỷ</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? 'Đang xoá...' : 'Xoá vĩnh viễn' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { usersApi, rolesApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import { useAuthStore } from '@/stores/auth.js'

const toast = useToastStore()
const auth  = useAuthStore()

const MIN_PASSWORD_LEN = 6   // khớp với backend (app/routers/admin.py)

const users   = ref([])
const total   = ref(0)
const loading = ref(true)
const page    = ref(1)
const PER_PAGE = 20

const search     = ref('')
const filterRole = ref('')
const busyId     = ref(null)

const deleteTarget = ref(null)
const deleteError  = ref('')
const deleting     = ref(false)

const myId = computed(() => auth.user?.id)
const canManageRoles = computed(() => auth.can('roles.view'))

const roles = ref([])
const selectedRole = computed(() => roles.value.find(r => r.id === form.role_id) || null)

const formModal = reactive({ open: false, id: null, saving: false, error: '' })
const form      = reactive({ full_name: '', email: '', phone: '', password: '', is_admin: false, is_active: true, role_id: null })

const isCreate = computed(() => formModal.id === null)
const isSelf   = computed(() => formModal.id !== null && formModal.id === myId.value)

const totalPages = computed(() => Math.ceil(total.value / PER_PAGE))
const pageNums   = computed(() => {
  const nums = [], c = page.value, l = totalPages.value
  for (let i = Math.max(1, c - 2); i <= Math.min(l, c + 2); i++) nums.push(i)
  return nums
})

async function loadRoles() {
  // Không có quyền xem vai trò thì vẫn cần danh sách để gán — bỏ qua nếu bị chặn
  try {
    roles.value = await rolesApi.list()
  } catch {
    roles.value = []
  }
}

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, per_page: PER_PAGE }
    if (search.value) params.search = search.value
    if (filterRole.value === 'admin') params.is_admin = true
    if (filterRole.value === 'user')  params.is_admin = false
    const res = await usersApi.list(params)
    users.value = res.results ?? res
    total.value = res.total ?? res.length
  } catch (e) {
    console.error('[UsersView] load error:', e)
    users.value = []
  } finally {
    loading.value = false
  }
}

function doSearch() { page.value = 1; load() }
function goPage(p)  { page.value = p; load() }

function resetForm(u) {
  form.full_name = u?.full_name || ''
  form.email     = u?.email     || ''
  form.phone     = u?.phone     || ''
  form.password  = ''
  form.is_admin  = !!u?.is_admin
  form.is_active = u ? !!u.is_active : true
  form.role_id   = u?.role_id ?? null
  formModal.error = ''
}

function openCreate() {
  formModal.id = null
  resetForm(null)
  formModal.open = true
}

function openEdit(u) {
  formModal.id = u.id
  resetForm(u)
  formModal.open = true
}

async function submitForm() {
  formModal.error = ''
  if (!form.email.trim()) { formModal.error = 'Vui lòng nhập email.'; return }
  if (isCreate.value && form.password.length < MIN_PASSWORD_LEN) {
    formModal.error = `Mật khẩu phải có ít nhất ${MIN_PASSWORD_LEN} ký tự.`
    return
  }
  if (!isCreate.value && form.password && form.password.length < MIN_PASSWORD_LEN) {
    formModal.error = `Mật khẩu mới phải có ít nhất ${MIN_PASSWORD_LEN} ký tự.`
    return
  }
  if (form.is_admin && !form.role_id) {
    formModal.error = 'Tài khoản admin phải được gán một vai trò.'
    return
  }

  formModal.saving = true
  try {
    const payload = {
      full_name: form.full_name,
      email:     form.email.trim(),
      phone:     form.phone,
      is_admin:  form.is_admin,
      is_active: form.is_active,
      role_id:   form.is_admin ? form.role_id : null,
    }
    if (isCreate.value) {
      payload.password = form.password
      await usersApi.create(payload)
      toast.success('Đã tạo tài khoản')
    } else {
      if (form.password) payload.password = form.password
      await usersApi.update(formModal.id, payload)
      toast.success('Cập nhật thành công')
    }
    formModal.open = false
    load()
  } catch (e) {
    formModal.error = String(e)
  } finally {
    formModal.saving = false
  }
}

async function toggleActive(u) {
  busyId.value = u.id
  try {
    await usersApi.update(u.id, { is_active: !u.is_active })
    toast.success(u.is_active ? `Đã khoá ${u.email}` : `Đã mở khoá ${u.email}`)
    load()
  } catch (e) {
    toast.error(String(e))
  } finally {
    busyId.value = null
  }
}

async function doDelete() {
  deleting.value = true
  deleteError.value = ''
  try {
    await usersApi.remove(deleteTarget.value.id)
    toast.success('Đã xoá tài khoản')
    deleteTarget.value = null
    load()
  } catch (e) {
    deleteError.value = String(e)
  } finally {
    deleting.value = false
  }
}

function formatDate(d) { return d ? new Date(d).toLocaleDateString('vi-VN') : '—' }

onMounted(() => { load(); loadRoles() })
</script>

<style scoped>
.toolbar { display: flex; align-items: center; gap: 10px; padding: 12px 16px; flex-wrap: wrap; }

.row-locked { opacity: .6; }

.self-tag {
  margin-left: 6px;
  padding: 1px 6px;
  border-radius: 999px;
  background: var(--bg);
  border: 1px solid var(--border);
  font-size: 10px;
  font-weight: 500;
  color: var(--text-2);
}

.error-box { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; }
</style>
