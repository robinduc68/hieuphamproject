<template>
  <div>
    <div class="page-header">
      <div class="page-title">Danh mục</div>
      <button v-if="auth.can('categories.create')" class="btn btn-primary" @click="openCatModal()">+ Thêm danh mục</button>
    </div>

    <div v-if="loading" class="card empty-state">Đang tải...</div>

    <div v-else class="cat-list">
      <div v-for="cat in categories" :key="cat.id" class="cat-block card">
        <!-- Category header -->
        <div class="cat-header">
          <div class="cat-info">
            <span class="cat-name">{{ cat.name }}</span>
            <span class="cat-slug">{{ cat.slug }}</span>
          </div>
          <div class="cat-actions">
            <button class="btn btn-secondary btn-sm" @click="openSubModal(cat)">+ Sub</button>
            <button class="btn btn-icon btn-sm" @click="openCatModal(cat)">✏️</button>
            <button v-if="auth.can('categories.delete')" class="btn btn-danger btn-sm" @click="deleteCat(cat)">✕</button>
          </div>
        </div>

        <!-- Subcategories -->
        <div v-if="cat.subcategories?.length" class="sub-list">
          <div v-for="sub in cat.subcategories" :key="sub.id" class="sub-item">
            <span class="sub-name">{{ sub.name }}</span>
            <span class="sub-slug">{{ sub.slug }}</span>
            <div class="sub-actions">
              <button class="btn btn-icon btn-sm" @click="openSubModal(cat, sub)">✏️</button>
              <button v-if="auth.can('categories.delete')" class="btn btn-danger btn-sm" @click="deleteSub(sub)">✕</button>
            </div>
          </div>
        </div>
        <div v-else class="sub-empty">Chưa có danh mục con</div>
      </div>
    </div>

    <!-- Category modal -->
    <div v-if="catModal.open" class="modal-overlay" @click.self="catModal.open=false">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">{{ catModal.target ? 'Sửa danh mục' : 'Thêm danh mục' }}</div>
          <button class="modal-close" @click="catModal.open=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Tên danh mục *</label>
            <input v-model="catForm.name" class="form-input" placeholder="Áo Dài" autofocus />
          </div>
          <div class="form-group">
            <label class="form-label">Slug *</label>
            <input v-model="catForm.slug" class="form-input" placeholder="ao-dai" />
          </div>
          <div class="form-group">
            <label class="form-label">Mô tả</label>
            <textarea v-model="catForm.description" class="form-textarea" rows="2" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="catModal.open=false">Huỷ</button>
          <button class="btn btn-primary" @click="saveCat" :disabled="catModal.saving">
            {{ catModal.saving ? 'Đang lưu...' : 'Lưu' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Sub modal -->
    <div v-if="subModal.open" class="modal-overlay" @click.self="subModal.open=false">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">{{ subModal.target ? 'Sửa danh mục con' : `Thêm con vào "${subModal.parent?.name}"` }}</div>
          <button class="modal-close" @click="subModal.open=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Tên *</label>
            <input v-model="subForm.name" class="form-input" placeholder="Áo Dài 2 Tà" autofocus />
          </div>
          <div class="form-group">
            <label class="form-label">Slug *</label>
            <input v-model="subForm.slug" class="form-input" placeholder="ao-dai-2-ta" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="subModal.open=false">Huỷ</button>
          <button class="btn btn-primary" @click="saveSub" :disabled="subModal.saving">
            {{ subModal.saving ? 'Đang lưu...' : 'Lưu' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { categoriesApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import { useAuthStore } from '@/stores/auth.js'

const toast      = useToastStore()
const categories = ref([])
const loading    = ref(true)

const catModal = reactive({ open: false, target: null, saving: false })
const catForm  = reactive({ name: '', slug: '', description: '' })

const subModal = reactive({ open: false, parent: null, target: null, saving: false })
const subForm  = reactive({ name: '', slug: '' })

async function load() {
  loading.value = true
  try { categories.value = await categoriesApi.list() }
  catch (e) {
    console.error('[CategoriesView] load error:', e)
    categories.value = []
  }
  finally { loading.value = false }
}

function openCatModal(cat = null) {
  catModal.target = cat
  catForm.name = cat?.name || ''; catForm.slug = cat?.slug || ''; catForm.description = cat?.description || ''
  catModal.open = true
}

async function saveCat() {
  catModal.saving = true
  try {
    if (catModal.target) await categoriesApi.update(catModal.target.id, catForm)
    else await categoriesApi.create(catForm)
    toast.success('Lưu thành công'); catModal.open = false; load()
  } catch (e) { toast.error(String(e)) }
  finally { catModal.saving = false }
}

async function deleteCat(cat) {
  if (!confirm(`Xoá danh mục "${cat.name}"?`)) return
  try { await categoriesApi.remove(cat.id); toast.success('Đã xoá'); load() }
  catch (e) { toast.error(String(e)) }
}

function openSubModal(parent, sub = null) {
  subModal.parent = parent; subModal.target = sub
  subForm.name = sub?.name || ''; subForm.slug = sub?.slug || ''
  subModal.open = true
}

async function saveSub() {
  subModal.saving = true
  try {
    if (subModal.target) await categoriesApi.updateSub(subModal.target.id, subForm)
    else await categoriesApi.createSub(subModal.parent.id, subForm)
    toast.success('Lưu thành công'); subModal.open = false; load()
  } catch (e) { toast.error(String(e)) }
  finally { subModal.saving = false }
}

async function deleteSub(sub) {
  if (!confirm(`Xoá "${sub.name}"?`)) return
  try { await categoriesApi.deleteSub(sub.id); toast.success('Đã xoá'); load() }
  catch (e) { toast.error(String(e)) }
}

onMounted(load)
</script>

<style scoped>
.cat-list { display: flex; flex-direction: column; gap: 16px; }
.cat-block { overflow: hidden; }
.cat-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid var(--border); }
.cat-info   { display: flex; align-items: center; gap: 12px; }
.cat-name   { font-weight: 600; font-size: 15px; }
.cat-slug   { font-size: 12px; color: var(--text-2); background: var(--bg); padding: 2px 8px; border-radius: 4px; }
.cat-actions{ display: flex; gap: 6px; }

.sub-list { padding: 8px 20px 12px; display: flex; flex-direction: column; gap: 4px; }
.sub-item { display: flex; align-items: center; gap: 12px; padding: 8px 12px; border-radius: 6px; background: var(--bg); }
.sub-name  { font-size: 13px; font-weight: 500; flex: 1; }
.sub-slug  { font-size: 11px; color: var(--text-2); }
.sub-actions{ display: flex; gap: 4px; margin-left: auto; }
.sub-empty { padding: 12px 20px; font-size: 13px; color: var(--text-2); }
</style>
