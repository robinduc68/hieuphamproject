<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">{{ isEdit ? 'Chỉnh sửa sản phẩm' : 'Thêm sản phẩm mới' }}</div>
        <div class="page-sub">{{ isEdit ? `ID: ${productId}` : 'Điền thông tin sản phẩm' }}</div>
      </div>
      <RouterLink to="/products" class="btn btn-secondary">← Quay lại</RouterLink>
    </div>

    <div v-if="loading" class="card empty-state">Đang tải...</div>

    <div v-else class="form-layout">

      <!-- ── Cột trái ── -->
      <div class="form-main">

        <!-- Thông tin cơ bản -->
        <div class="card form-section">
          <div class="section-title">Thông tin cơ bản</div>
          <div class="form-group">
            <label class="form-label">Tên sản phẩm *</label>
            <input v-model="form.name" class="form-input" placeholder="VD: Áo dài lụa tơ tằm..." @input="autoSlug" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Slug *</label>
              <input v-model="form.slug" class="form-input" placeholder="ao-dai-lua-to-tam" />
              <span class="form-hint">URL thân thiện, không dấu, dùng dấu -</span>
            </div>
            <div class="form-group">
              <label class="form-label">Giá (VNĐ) *</label>
              <input v-model.number="form.price" type="number" min="0" class="form-input" placeholder="5000000" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Giá gốc / Giá so sánh (VNĐ)</label>
            <input v-model.number="form.compare_at_price" type="number" min="0" class="form-input" placeholder="Để trống nếu không khuyến mãi" />
            <span class="form-hint">Hiển thị gạch ngang nếu đang sale</span>
          </div>
          <div class="form-group">
            <label class="form-label">Mô tả</label>
            <textarea v-model="form.description" class="form-textarea" rows="4" placeholder="Mô tả ngắn gọn về sản phẩm..." />
          </div>
        </div>

        <!-- Chi tiết -->
        <div class="card form-section">
          <div class="section-title">Chi tiết sản phẩm</div>
          <div class="form-group">
            <label class="form-label">Chất liệu vải</label>
            <textarea v-model="form.fabric" class="form-textarea" rows="2" placeholder="Lụa tơ tằm 100%..." />
          </div>
          <div class="form-group">
            <label class="form-label">Hướng dẫn bảo quản</label>
            <textarea v-model="form.care_instructions" class="form-textarea" rows="2" placeholder="Giặt tay, không vắt..." />
          </div>
          <div class="form-group">
            <label class="form-label">Thông tin giao hàng</label>
            <textarea v-model="form.shipping_info" class="form-textarea" rows="2" placeholder="Giao hàng 3-5 ngày..." />
          </div>
        </div>

        <!-- Quản lý ảnh -->
        <div class="card form-section">
          <div class="section-title">Quản lý ảnh</div>

          <div v-if="!isEdit" class="create-note">
            💡 Lưu sản phẩm trước, sau đó bạn sẽ được chuyển sang trang chỉnh sửa để upload ảnh.
          </div>

          <template v-else>
            <!-- Danh sách ảnh hiện tại -->
            <div class="images-grid" v-if="images.length">
              <div v-for="img in images" :key="img.id" class="img-item" :class="{primary: img.is_primary}">
                <img :src="img.url" :alt="img.alt_text || ''" />
                <div class="img-overlay">
                  <button class="img-btn" @click="setPrimary(img)" title="Đặt làm ảnh chính">
                    <svg viewBox="0 0 16 16" fill="currentColor" style="width:13px;height:13px"><path d="M8 1l2 4h4l-3 3 1 5L8 11l-4 2 1-5L2 5h4z"/></svg>
                  </button>
                  <button class="img-btn danger" @click="deleteImage(img)" title="Xoá ảnh">
                    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px"><path d="M2 4h12M5 4V2h6v2M6 7v5M10 7v5M3 4l1 10h8l1-10"/></svg>
                  </button>
                </div>
                <div class="img-primary-tag" v-if="img.is_primary">Ảnh chính</div>
              </div>
            </div>
            <div v-else class="empty-state" style="padding:24px;font-size:13px">Chưa có ảnh nào</div>

            <!-- Upload -->
            <div class="upload-area" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
              <input ref="fileInput" type="file" accept="image/*" multiple style="display:none" @change="handleFileSelect" />
              <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" style="width:36px;height:36px;color:var(--text-2)"><path d="M24 8v24M12 20l12-12 12 12"/><path d="M8 36h32"/></svg>
              <p>Kéo thả hoặc <strong>click để chọn ảnh</strong></p>
              <p style="font-size:12px;color:var(--text-2)">PNG, JPG, WEBP — tối đa 10MB mỗi ảnh</p>
            </div>

            <div v-if="uploading" class="upload-progress">
              Đang upload {{ uploadProgress }}...
            </div>
          </template>
        </div>

        <!-- Kích thước -->
        <div class="card form-section">
          <div class="section-title">Kích thước</div>

          <div v-if="!isEdit" class="create-note">
            💡 Lưu sản phẩm trước, sau đó bạn có thể thêm kích thước.
          </div>

          <template v-else>
            <div class="sizes-row" v-if="sizes.length">
              <span v-for="s in sizes" :key="s.id" class="size-chip" :class="{unavailable: !s.in_stock}">
                {{ s.size }}
                <button @click="toggleSize(s)" class="size-toggle" :title="s.in_stock ? 'Tắt' : 'Bật'">{{ s.in_stock ? '✓' : '✕' }}</button>
                <button @click="deleteSize(s)" class="size-del" title="Xoá">×</button>
              </span>
            </div>
            <div v-else style="font-size:13px;color:var(--text-2);margin-bottom:12px">Chưa có size nào</div>

            <div style="display:flex;gap:8px;margin-top:12px">
              <input v-model="newSize" class="form-input" placeholder="VD: S, M, L, 36, 38..." style="max-width:160px" @keyup.enter="addSize" />
              <button class="btn btn-secondary" @click="addSize">Thêm size</button>
            </div>
          </template>
        </div>

      </div>

      <!-- ── Cột phải ── -->
      <div class="form-side">

        <div class="card form-section">
          <div class="section-title">Phân loại</div>
          <div class="form-group">
            <label class="form-label">Danh mục</label>
            <select v-model="form.category_id" class="form-select">
              <option value="">Chọn danh mục</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
            <span v-if="!categories.length" class="form-hint" style="color:var(--brand)">Chưa có danh mục nào</span>
          </div>
          <div class="form-group">
            <label class="form-label">Màu chính (HEX)</label>
            <div style="display:flex;gap:8px;align-items:center">
              <input v-model="form.primary_color" type="color" style="width:40px;height:36px;padding:2px;border:1px solid var(--border);border-radius:6px;cursor:pointer" />
              <input v-model="form.primary_color" class="form-input" placeholder="#B8965A" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Thứ tự hiển thị</label>
            <input v-model.number="form.sort_order" type="number" class="form-input" placeholder="0" />
          </div>
        </div>

        <div class="card form-section">
          <div class="section-title">Trạng thái</div>
          <label class="toggle-row">
            <span>Hiển thị trên cửa hàng</span>
            <div class="toggle" :class="{on: form.is_active}" @click="form.is_active = !form.is_active" />
          </label>
          <label class="toggle-row">
            <span>Sản phẩm mới</span>
            <div class="toggle" :class="{on: form.is_new}" @click="form.is_new = !form.is_new" />
          </label>
          <label class="toggle-row">
            <span>Nổi bật</span>
            <div class="toggle" :class="{on: form.is_featured}" @click="form.is_featured = !form.is_featured" />
          </label>
        </div>

        <div v-if="saveError" class="error-box">{{ saveError }}</div>

        <button class="btn btn-primary" style="width:100%;justify-content:center;padding:12px" @click="save" :disabled="saving">
          {{ saving ? 'Đang lưu...' : (isEdit ? 'Lưu thay đổi' : 'Tạo sản phẩm') }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productsApi, categoriesApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'

const route  = useRoute()
const router = useRouter()
const toast  = useToastStore()

const productId = computed(() => route.params.id)
const isEdit    = computed(() => !!productId.value)

const loading        = ref(false)
const saving         = ref(false)
const saveError      = ref('')
const uploading      = ref(false)
const uploadProgress = ref('')
const fileInput      = ref(null)

const images    = ref([])
const sizes     = ref([])
const categories = ref([])
const newSize   = ref('')

const form = ref({
  name: '', slug: '', price: null, compare_at_price: null,
  description: '', fabric: '', care_instructions: '', shipping_info: '',
  category_id: '', primary_color: '', sort_order: 0,
  is_active: true, is_new: false, is_featured: false,
})

// ── Vietnamese slug generator ─────────────────────────────────────────────
const VI_MAP = {
  à:'a',á:'a',ả:'a',ã:'a',ạ:'a',ă:'a',ắ:'a',ằ:'a',ẳ:'a',ẵ:'a',ặ:'a',
  â:'a',ấ:'a',ầ:'a',ẩ:'a',ẫ:'a',ậ:'a',
  è:'e',é:'e',ẻ:'e',ẽ:'e',ẹ:'e',ê:'e',ế:'e',ề:'e',ể:'e',ễ:'e',ệ:'e',
  ì:'i',í:'i',ỉ:'i',ĩ:'i',ị:'i',
  ò:'o',ó:'o',ỏ:'o',õ:'o',ọ:'o',ô:'o',ố:'o',ồ:'o',ổ:'o',ỗ:'o',ộ:'o',
  ơ:'o',ớ:'o',ờ:'o',ở:'o',ỡ:'o',ợ:'o',
  ù:'u',ú:'u',ủ:'u',ũ:'u',ụ:'u',ư:'u',ứ:'u',ừ:'u',ử:'u',ữ:'u',ự:'u',
  ỳ:'y',ý:'y',ỷ:'y',ỹ:'y',ỵ:'y',đ:'d',
}

function toSlug(str) {
  return str.toLowerCase()
    .split('').map(c => VI_MAP[c] ?? c).join('')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim().replace(/\s+/g, '-').replace(/-+/g, '-')
}

let slugTouched = false  // nếu user tự sửa slug thì không auto-gen nữa

function autoSlug() {
  if (!slugTouched) form.value.slug = toSlug(form.value.name)
}

watch(() => form.value.slug, (val, old) => {
  if (val !== toSlug(form.value.name)) slugTouched = true
})

// ── Load data ─────────────────────────────────────────────────────────────
async function loadData() {
  loading.value = true
  saveError.value = ''
  try {
    const cats = await categoriesApi.list()
    categories.value = Array.isArray(cats) ? cats : (cats?.results ?? [])

    if (isEdit.value) {
      const p = await productsApi.get(productId.value)
      Object.assign(form.value, {
        name:              p.name,
        slug:              p.slug,
        price:             Number(p.price),
        compare_at_price:  p.compare_at_price ? Number(p.compare_at_price) : null,
        description:       p.description       || '',
        fabric:            p.fabric            || '',
        care_instructions: p.care_instructions || '',
        shipping_info:     p.shipping_info     || '',
        category_id:       p.category_id       || '',
        primary_color:     p.primary_color     || p.images?.[0]?.color_hex || '',
        sort_order:        p.sort_order        || 0,
        is_active:         p.is_active  ?? true,
        is_new:            p.is_new     ?? false,
        is_featured:       p.is_featured ?? false,
      })
      images.value = p.images || []
      sizes.value  = p.sizes  || []
      slugTouched  = true  // không auto-gen slug khi edit
    }
  } catch (e) {
    toast.error('Lỗi tải dữ liệu: ' + e)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
watch(() => route.params.id, loadData)

// ── Save ──────────────────────────────────────────────────────────────────
async function save() {
  saveError.value = ''

  if (!form.value.name.trim()) { saveError.value = 'Vui lòng nhập tên sản phẩm.'; return }
  if (!form.value.slug.trim()) { saveError.value = 'Vui lòng nhập slug.'; return }
  if (!form.value.price)       { saveError.value = 'Vui lòng nhập giá.'; return }

  saving.value = true
  try {
    const data = { ...form.value }
    if (!data.category_id)      delete data.category_id
    if (!data.compare_at_price) delete data.compare_at_price

    if (isEdit.value) {
      await productsApi.update(productId.value, data)
      toast.success('Đã lưu thay đổi')
    } else {
      const created = await productsApi.create({ ...data, sizes: [] })
      toast.success('Tạo sản phẩm thành công! Giờ bạn có thể upload ảnh và thêm size.')
      router.push(`/products/${created.id}/edit`)
    }
  } catch (e) {
    saveError.value = typeof e === 'string' ? e : (e?.message || 'Có lỗi xảy ra')
  } finally {
    saving.value = false
  }
}

// ── Upload images ─────────────────────────────────────────────────────────
async function handleFileSelect(e) { await uploadFiles(Array.from(e.target.files)); e.target.value = '' }
async function handleDrop(e) { await uploadFiles(Array.from(e.dataTransfer.files)) }

async function uploadFiles(files) {
  if (!files.length) return
  uploading.value = true
  for (let i = 0; i < files.length; i++) {
    uploadProgress.value = `${i + 1}/${files.length}`
    const fd = new FormData()
    fd.append('file', files[i])
    if (form.value.primary_color) fd.append('color_hex', form.value.primary_color)
    try {
      const img = await productsApi.uploadImage(productId.value, fd)
      images.value.push({
        id: img.id, url: img.url, alt_text: '',
        sort_order: img.position, is_primary: images.value.length === 0,
      })
    } catch (e) { toast.error(`Lỗi upload ảnh: ${e}`) }
  }
  uploading.value = false
  uploadProgress.value = ''
  if (images.value.length) toast.success('Upload ảnh thành công')
}

async function setPrimary(img) {
  try {
    await productsApi.updateImage(productId.value, img.id, { is_primary: true })
    images.value.forEach(i => i.is_primary = (i.id === img.id))
  } catch (e) { toast.error(String(e)) }
}

async function deleteImage(img) {
  if (!confirm('Xoá ảnh này?')) return
  try {
    await productsApi.deleteImage(productId.value, img.id)
    images.value = images.value.filter(i => i.id !== img.id)
  } catch (e) { toast.error(String(e)) }
}

// ── Sizes ─────────────────────────────────────────────────────────────────
async function addSize() {
  const sz = newSize.value.trim().toUpperCase()
  if (!sz) return
  try {
    const s = await productsApi.addSize(productId.value, { size: sz })
    sizes.value.push(s)
    newSize.value = ''
  } catch (e) { toast.error(String(e)) }
}

async function toggleSize(s) {
  try {
    const updated = await productsApi.updateSize(productId.value, s.id, { is_available: !s.in_stock })
    s.in_stock = updated.in_stock
  } catch (e) { toast.error(String(e)) }
}

async function deleteSize(s) {
  try {
    await productsApi.deleteSize(productId.value, s.id)
    sizes.value = sizes.value.filter(x => x.id !== s.id)
  } catch (e) { toast.error(String(e)) }
}
</script>

<style scoped>
.form-layout { display: flex; gap: 20px; align-items: flex-start; }
.form-main   { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 16px; }
.form-side   { width: 280px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px; }

.form-section  { padding: 20px; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.form-row      { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.create-note {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 13px;
  color: #1d4ed8;
}

/* Images */
.images-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px; }
.img-item { position: relative; aspect-ratio: 3/4; border-radius: 8px; overflow: hidden; border: 2px solid transparent; }
.img-item.primary { border-color: var(--brand); }
.img-item img { width: 100%; height: 100%; object-fit: cover; display: block; }
.img-overlay {
  position: absolute; inset: 0; background: rgba(0,0,0,.5);
  display: flex; align-items: center; justify-content: center; gap: 8px;
  opacity: 0; transition: opacity .2s;
}
.img-item:hover .img-overlay { opacity: 1; }
.img-btn { width: 32px; height: 32px; border-radius: 50%; border: none; background: rgba(255,255,255,.9); color: var(--text); cursor: pointer; display: flex; align-items: center; justify-content: center; }
.img-btn.danger { color: #DC2626; }
.img-primary-tag { position: absolute; bottom: 0; left: 0; right: 0; background: var(--brand); color: #fff; font-size: 10px; font-weight: 600; text-align: center; padding: 3px; }

.upload-area {
  border: 2px dashed var(--border);
  border-radius: 8px;
  padding: 28px;
  text-align: center;
  cursor: pointer;
  transition: border-color .2s;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.upload-area:hover { border-color: var(--brand); }
.upload-area p { font-size: 13px; color: var(--text); margin: 0; }

.upload-progress { margin-top: 10px; font-size: 13px; color: var(--text-2); }

/* Sizes */
.sizes-row { display: flex; flex-wrap: wrap; gap: 8px; }
.size-chip {
  display: flex; align-items: center; gap: 4px;
  padding: 6px 10px; border-radius: 6px;
  background: var(--bg); border: 1px solid var(--border);
  font-size: 13px; font-weight: 500;
}
.size-chip.unavailable { opacity: .5; text-decoration: line-through; }
.size-toggle, .size-del {
  background: none; border: none; cursor: pointer;
  font-size: 12px; color: var(--text-2); padding: 0 2px; line-height: 1;
}
.size-toggle:hover { color: #16a34a; }
.size-del:hover    { color: #DC2626; }

/* Toggle */
.toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); cursor: pointer; font-size: 13px; }
.toggle-row:last-child { border-bottom: none; }
.toggle { width: 36px; height: 20px; border-radius: 10px; background: #D1D5DB; position: relative; transition: background .2s; flex-shrink: 0; }
.toggle.on { background: var(--brand); }
.toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; border-radius: 50%; background: #fff; transition: transform .2s; }
.toggle.on::after { transform: translateX(16px); }

.error-box { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; }

@media (max-width: 900px) {
  .form-layout { flex-direction: column; }
  .form-side { width: 100%; }
  .images-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
