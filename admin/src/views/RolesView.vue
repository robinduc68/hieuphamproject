<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Vai trò & phân quyền</div>
        <div class="page-sub">{{ roles.length }} vai trò</div>
      </div>
      <button v-if="auth.can('roles.manage')" class="btn btn-primary" @click="openCreate">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M8 2v12M2 8h12"/></svg>
        Thêm vai trò
      </button>
    </div>

    <div class="card intro">
      Vai trò quyết định một tài khoản admin <strong>vào được tab nào</strong> và
      <strong>bấm được nút nào</strong> trong tab đó. Gán vai trò cho tài khoản ở mục
      <RouterLink to="/users">Người dùng</RouterLink>. Hiện quyền chỉ dùng để ẩn/hiện giao diện —
      tài khoản admin nào cũng gọi được API trực tiếp, nên chỉ cấp quyền admin cho người tin tưởng.
    </div>

    <div class="card" style="margin-top:16px">
      <div v-if="loading" class="empty-state">Đang tải...</div>
      <div v-else-if="!roles.length" class="empty-state">Chưa có vai trò nào</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Vai trò</th>
              <th>Quyền</th>
              <th style="width:120px">Tài khoản</th>
              <th style="width:140px">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in roles" :key="r.id">
              <td>
                <div class="role-name">
                  {{ r.name }}
                  <span v-if="r.is_system" class="sys-tag">gốc</span>
                </div>
                <div v-if="r.description" class="role-desc">{{ r.description }}</div>
              </td>
              <td>
                <span v-if="isFullAccess(r)" class="badge badge-confirmed">Toàn quyền</span>
                <div v-else class="perm-chips">
                  <span v-for="g in groupSummary(r)" :key="g.key" class="perm-chip">
                    {{ g.label }} <b>{{ g.count }}/{{ g.total }}</b>
                  </span>
                  <span v-if="!groupSummary(r).length" style="font-size:12px;color:var(--text-2)">
                    Chưa tick quyền nào
                  </span>
                </div>
              </td>
              <td>{{ r.user_count }}</td>
              <td>
                <div style="display:flex;gap:6px">
                  <button class="btn btn-secondary btn-sm" :disabled="!auth.can('roles.manage')" @click="openEdit(r)">
                    {{ r.is_system ? 'Xem' : 'Sửa' }}
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    :disabled="!auth.can('roles.manage') || r.is_system || r.user_count > 0"
                    :title="r.is_system ? 'Vai trò gốc không xoá được'
                            : (r.user_count > 0 ? 'Còn tài khoản đang dùng vai trò này' : '')"
                    @click="deleteTarget = r"
                  >Xoá</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal tạo / sửa -->
    <div v-if="modal.open" class="modal-overlay" @click.self="modal.open=false">
      <div class="modal modal-lg">
        <div class="modal-header">
          <div class="modal-title">
            {{ modal.id === null ? 'Thêm vai trò' : (form.is_system ? 'Vai trò gốc' : 'Sửa vai trò') }}
          </div>
          <button class="modal-close" @click="modal.open=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Tên vai trò *</label>
              <input v-model="form.name" class="form-input" placeholder="VD: Nhân viên kho" :disabled="form.is_system" />
            </div>
            <div class="form-group">
              <label class="form-label">Mô tả</label>
              <input v-model="form.description" class="form-input" placeholder="Vai trò này làm những gì" />
            </div>
          </div>

          <div v-if="form.is_system" class="intro" style="margin-bottom:16px">
            Đây là vai trò gốc <strong>toàn quyền</strong> — luôn có mọi quyền, kể cả quyền
            thêm sau này. Không sửa được danh sách quyền để tránh trường hợp không còn ai
            vào được trang quản trị.
          </div>

          <template v-else>
            <div class="perm-head">
              <span class="form-label" style="margin:0">Quyền</span>
              <div style="display:flex;gap:8px">
                <button class="btn btn-secondary btn-sm" @click="selectAll(true)">Chọn tất cả</button>
                <button class="btn btn-secondary btn-sm" @click="selectAll(false)">Bỏ chọn tất cả</button>
              </div>
            </div>

            <div v-for="g in catalog" :key="g.key" class="perm-group">
              <label class="perm-group-head">
                <input
                  type="checkbox"
                  :checked="allChecked(g)"
                  :indeterminate.prop="someChecked(g)"
                  @change="toggleGroup(g, $event.target.checked)"
                />
                <span class="perm-group-label">{{ g.label }}</span>
                <span class="perm-group-count">{{ checkedCount(g) }}/{{ g.permissions.length }}</span>
              </label>
              <div class="perm-items">
                <label v-for="p in g.permissions" :key="p.code" class="perm-item">
                  <input type="checkbox" :value="p.code" v-model="form.permissions" />
                  <span>
                    {{ p.label }}
                    <code class="perm-code">{{ p.code }}</code>
                  </span>
                </label>
              </div>
            </div>
          </template>

          <div v-if="modal.error" class="error-box" style="margin-top:16px">{{ modal.error }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="modal.open=false">
            {{ form.is_system ? 'Đóng' : 'Huỷ' }}
          </button>
          <button class="btn btn-primary" @click="submit" :disabled="modal.saving">
            {{ modal.saving ? 'Đang lưu...' : (modal.id === null ? 'Tạo vai trò' : 'Lưu') }}
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
          <p>Xoá vai trò <strong>{{ deleteTarget.name }}</strong>?</p>
          <div v-if="deleteError" class="error-box" style="margin-top:14px">{{ deleteError }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="deleteTarget=null">Huỷ</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? 'Đang xoá...' : 'Xoá vai trò' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { rolesApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import { useAuthStore } from '@/stores/auth.js'

const toast = useToastStore()
const auth  = useAuthStore()

const WILDCARD = '*'

const roles   = ref([])
const catalog = ref([])
const loading = ref(true)

const deleteTarget = ref(null)
const deleteError  = ref('')
const deleting     = ref(false)

const modal = reactive({ open: false, id: null, saving: false, error: '' })
const form  = reactive({ name: '', description: '', permissions: [], is_system: false })

function isFullAccess(role) {
  return role.permissions?.includes(WILDCARD)
}

/** Tóm tắt "Sản phẩm 3/4" cho từng nhóm có ít nhất 1 quyền được tick. */
function groupSummary(role) {
  const granted = new Set(role.permissions || [])
  return catalog.value
    .map(g => ({
      key:   g.key,
      label: g.label,
      total: g.permissions.length,
      count: g.permissions.filter(p => granted.has(p.code)).length,
    }))
    .filter(g => g.count > 0)
}

function checkedCount(group) {
  return group.permissions.filter(p => form.permissions.includes(p.code)).length
}
function allChecked(group)  { return checkedCount(group) === group.permissions.length }
function someChecked(group) { const n = checkedCount(group); return n > 0 && n < group.permissions.length }

function toggleGroup(group, checked) {
  const codes = group.permissions.map(p => p.code)
  form.permissions = checked
    ? [...new Set([...form.permissions, ...codes])]
    : form.permissions.filter(c => !codes.includes(c))
}

function selectAll(checked) {
  form.permissions = checked
    ? catalog.value.flatMap(g => g.permissions.map(p => p.code))
    : []
}

async function load() {
  loading.value = true
  try {
    const [list, cat] = await Promise.all([rolesApi.list(), rolesApi.permissions()])
    roles.value   = list
    catalog.value = cat
  } catch (e) {
    toast.error('Lỗi tải vai trò: ' + e)
    roles.value = []
  } finally {
    loading.value = false
  }
}

function openCreate() {
  modal.id = null
  modal.error = ''
  Object.assign(form, { name: '', description: '', permissions: [], is_system: false })
  modal.open = true
}

function openEdit(r) {
  modal.id = r.id
  modal.error = ''
  Object.assign(form, {
    name:        r.name,
    description: r.description || '',
    permissions: isFullAccess(r) ? [] : [...(r.permissions || [])],
    is_system:   r.is_system,
  })
  modal.open = true
}

async function submit() {
  modal.error = ''
  if (!form.name.trim()) { modal.error = 'Vui lòng nhập tên vai trò.'; return }

  modal.saving = true
  try {
    const payload = {
      name:        form.name.trim(),
      description: form.description,
      permissions: form.permissions,
    }
    if (modal.id === null) {
      await rolesApi.create(payload)
      toast.success('Đã tạo vai trò')
    } else {
      await rolesApi.update(modal.id, payload)
      toast.success('Đã lưu vai trò')
      // Sửa vai trò của chính mình thì nạp lại quyền để giao diện khớp ngay
      if (modal.id === auth.user?.role_id) await auth.refresh()
    }
    modal.open = false
    load()
  } catch (e) {
    modal.error = String(e)
  } finally {
    modal.saving = false
  }
}

async function doDelete() {
  deleting.value = true
  deleteError.value = ''
  try {
    await rolesApi.remove(deleteTarget.value.id)
    toast.success('Đã xoá vai trò')
    deleteTarget.value = null
    load()
  } catch (e) {
    deleteError.value = String(e)
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.intro {
  padding: 14px 16px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-2);
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
}
.intro a { color: var(--brand); }

.role-name { font-weight: 600; display: flex; align-items: center; gap: 6px; }
.role-desc { font-size: 12px; color: var(--text-2); margin-top: 2px; max-width: 420px; }
.sys-tag {
  padding: 1px 6px; border-radius: 999px;
  background: var(--bg); border: 1px solid var(--border);
  font-size: 10px; font-weight: 500; color: var(--text-2);
}

.perm-chips { display: flex; flex-wrap: wrap; gap: 6px; max-width: 460px; }
.perm-chip {
  padding: 2px 8px; border-radius: 999px;
  background: var(--bg); border: 1px solid var(--border);
  font-size: 11px; color: var(--text-2);
}
.perm-chip b { color: var(--text); font-weight: 600; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.perm-head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 12px; padding-top: 4px;
}

.perm-group { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 10px; }
.perm-group-head {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; background: var(--bg);
  border-bottom: 1px solid var(--border);
  border-radius: 8px 8px 0 0;
  cursor: pointer;
}
.perm-group-label { font-size: 13px; font-weight: 600; }
.perm-group-count { margin-left: auto; font-size: 12px; color: var(--text-2); }

.perm-items {
  display: grid; grid-template-columns: 1fr 1fr; gap: 8px 16px;
  padding: 12px 14px;
}
.perm-item { display: flex; align-items: flex-start; gap: 8px; font-size: 13px; cursor: pointer; }
.perm-item input { margin-top: 3px; flex-shrink: 0; }
.perm-code {
  display: block; font-size: 11px; color: var(--text-2);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

.error-box { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; }

@media (max-width: 800px) {
  .form-row, .perm-items { grid-template-columns: 1fr; }
}

@media (max-width: 560px) {
  .role-desc, .perm-chips { max-width: none; }
  .perm-head { flex-direction: column; align-items: stretch; gap: 8px; }
  .perm-head > div { display: flex; gap: 8px; }
  .perm-head .btn { flex: 1; justify-content: center; }
}
</style>
