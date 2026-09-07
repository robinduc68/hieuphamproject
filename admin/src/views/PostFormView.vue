<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">{{ isEdit ? 'Chỉnh sửa bài viết' : 'Viết bài mới' }}</div>
        <div class="page-sub">{{ isEdit ? `ID: ${postId}` : 'Bài viết hiện ở trang Tin tức ngoài website' }}</div>
      </div>
      <div class="header-actions">
        <a v-if="publicUrl" :href="publicUrl" target="_blank" rel="noopener"
           class="btn btn-secondary" title="Mở bài viết ngoài website ở tab mới">
          Xem trên web ↗
        </a>
        <RouterLink to="/posts" class="btn btn-secondary">← Quay lại</RouterLink>
      </div>
    </div>

    <div v-if="loading" class="card empty-state">Đang tải...</div>

    <div v-else class="form-layout">

      <!-- ── Cột trái ── -->
      <div class="form-main">

        <div class="card form-section">
          <div class="section-title">Nội dung bài viết</div>

          <div class="form-group">
            <label class="form-label">Tiêu đề *</label>
            <input v-model="form.title" class="form-input" placeholder="VD: Cách chọn vải lụa chuẩn..." @input="autoSlug" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Slug *</label>
              <input v-model="form.slug" class="form-input" placeholder="cach-chon-vai-lua-chuan" />
              <span class="form-hint">Địa chỉ bài viết: /tin-tuc/{{ form.slug || 'slug-bai-viet' }}</span>
            </div>
            <div class="form-group">
              <label class="form-label">Nhãn</label>
              <input v-model="form.tag" class="form-input" list="post-tags" placeholder="VD: Kiến thức vải" />
              <datalist id="post-tags">
                <option v-for="t in tagSuggestions" :key="t" :value="t" />
              </datalist>
              <span class="form-hint">Chữ nhỏ màu đỏ trên card ngoài trang Tin tức.</span>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Mô tả ngắn</label>
            <input v-model="form.subtitle" class="form-input" placeholder="Câu dẫn hiện dưới tiêu đề ở trang chi tiết" />
          </div>

          <div class="form-group">
            <label class="form-label">Tóm tắt</label>
            <textarea v-model="form.excerpt" class="form-input" rows="2"
                      placeholder="Vài dòng tóm tắt hiện trên card ở trang danh sách Tin tức" />
            <span class="form-hint">Bỏ trống thì card ngoài web sẽ dùng mô tả ngắn ở trên.</span>
          </div>

          <div class="form-group">
            <label class="form-label">Thân bài</label>
            <RichTextEditor v-model="form.content" :min-height="360"
                            placeholder="Soạn nội dung bài viết — tiêu đề, in đậm/nghiêng, danh sách, trích dẫn, ảnh..." />
            <span class="form-hint">Dùng thanh công cụ để thêm tiêu đề, danh sách, liên kết và ảnh chèn giữa bài.</span>
          </div>
        </div>

        <div class="card form-section">
          <div class="section-title">Ảnh bìa</div>
          <p class="form-hint" style="margin-bottom:14px">
            Ảnh này vừa là hình trên card ở trang danh sách, vừa là ảnh lớn đầu trang chi tiết.
            Chưa có ảnh thì web dùng nền màu bên dưới.
          </p>

          <div class="cover-row">
            <div class="cover-preview" :style="{ background: form.cover_color || '#E5E7EB' }">
              <img v-if="form.cover_image" :src="form.cover_image" alt="Ảnh bìa" />
            </div>
            <div class="cover-fields">
              <div class="form-group">
                <label class="form-label">Đường dẫn ảnh</label>
                <input v-model="form.cover_image" class="form-input" placeholder="/media/... hoặc https://..." />
              </div>
              <div class="upload-row">
                <button class="btn btn-secondary" :disabled="uploading" @click="$refs.coverInput.click()">
                  {{ uploading ? 'Đang tải lên...' : 'Tải ảnh bìa lên' }}
                </button>
                <button v-if="form.cover_image" class="btn btn-secondary" @click="form.cover_image = ''">
                  Bỏ ảnh
                </button>
                <input ref="coverInput" type="file" accept="image/*" style="display:none" @change="onCoverSelected" />
              </div>
              <div class="form-group" style="margin-top:14px">
                <label class="form-label">Nền thay ảnh (khi chưa có ảnh bìa)</label>
                <input v-model="form.cover_color" class="form-input" placeholder="linear-gradient(135deg, #C8A898 0%, #D0B0A0 100%)" />
                <span class="form-hint">Nhận mã màu (#C8A898) hoặc dải gradient CSS.</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ── Cột phải ── -->
      <div class="form-side">

        <div class="card form-section">
          <div class="section-title">Đăng bài</div>
          <div class="form-group">
            <label class="form-label">Ngày đăng</label>
            <input v-model="form.published_at" type="date" class="form-input" />
            <span class="form-hint">Ngày hiện trên card. Bỏ trống cũng được.</span>
          </div>
          <div class="form-group">
            <label class="form-label">Thứ tự hiển thị</label>
            <input v-model.number="form.sort_order" type="number" class="form-input" placeholder="0" />
            <span class="form-hint">Số nhỏ đứng trước. Bằng nhau thì bài mới hơn đứng trước.</span>
          </div>
          <label class="toggle-row">
            <span>Đang đăng</span>
            <div class="toggle" :class="{on: form.is_published}" @click="form.is_published = !form.is_published" />
          </label>
          <span class="form-hint">Tắt = bài chỉ nằm trong admin, khách không thấy ngoài website.</span>
        </div>

        <div v-if="saveError" class="error-box">{{ saveError }}</div>

        <button class="btn btn-primary" style="width:100%;justify-content:center;padding:12px" @click="save" :disabled="saving">
          {{ saving ? 'Đang lưu...' : (isEdit ? 'Lưu thay đổi' : 'Đăng bài') }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postsApi, uploadsApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import RichTextEditor from '@/components/RichTextEditor.vue'
import { toSlug } from '@/utils/slug.js'
import { siteUrl } from '@/utils/siteUrl.js'

const route  = useRoute()
const router = useRouter()
const toast  = useToastStore()

const postId = computed(() => route.params.id)
const isEdit = computed(() => !!postId.value)

const loading   = ref(false)
const saving    = ref(false)
const uploading = ref(false)
const saveError = ref('')
const coverInput = ref(null)

// Link sang bài viết ngoài web — xem được cả bài đang để nháp.
const publicUrl = computed(() =>
  isEdit.value && form.value.slug ? siteUrl(`/tin-tuc/${form.value.slug}`) : ''
)

const tagSuggestions = ['Kiến thức vải', 'Tips mặc đẹp', 'Xu hướng', 'Chăm sóc', 'Phong cách']

const form = ref({
  title: '', slug: '', tag: '', subtitle: '', excerpt: '', content: '',
  cover_image: '', cover_color: '', published_at: todayIso(),
  is_published: true, sort_order: 0,
})

function todayIso() {
  return new Date().toISOString().slice(0, 10)
}

let slugTouched = false   // user tự sửa slug thì không auto-gen nữa

function autoSlug() {
  if (!slugTouched) form.value.slug = toSlug(form.value.title)
}

watch(() => form.value.slug, (val) => {
  if (val !== toSlug(form.value.title)) slugTouched = true
})

async function loadData() {
  saveError.value = ''
  if (!isEdit.value) return
  loading.value = true
  try {
    const p = await postsApi.get(postId.value)
    Object.assign(form.value, {
      title:        p.title || '',
      slug:         p.slug  || '',
      tag:          p.tag      || '',
      subtitle:     p.subtitle || '',
      excerpt:      p.excerpt  || '',
      content:      p.content  || '',
      cover_image:  p.cover_image || '',
      cover_color:  p.cover_color || '',
      published_at: p.published_at ? String(p.published_at).slice(0, 10) : '',
      is_published: p.is_published ?? true,
      sort_order:   p.sort_order   ?? 0,
    })
    slugTouched = true
  } catch (e) {
    toast.error('Lỗi tải bài viết: ' + e)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
watch(() => route.params.id, loadData)

async function onCoverSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await uploadsApi.image(fd)
    form.value.cover_image = res.url
    toast.success('Đã tải ảnh bìa lên')
  } catch (err) {
    toast.error('Lỗi tải ảnh: ' + err)
  } finally {
    uploading.value = false
  }
}

async function save() {
  saveError.value = ''
  if (!form.value.title.trim()) { saveError.value = 'Vui lòng nhập tiêu đề bài viết.'; return }
  if (!form.value.slug.trim())  { saveError.value = 'Vui lòng nhập slug.'; return }

  saving.value = true
  try {
    const data = { ...form.value, published_at: form.value.published_at || null }
    if (isEdit.value) {
      await postsApi.update(postId.value, data)
      toast.success('Đã lưu bài viết')
    } else {
      const created = await postsApi.create(data)
      toast.success('Đã đăng bài viết')
      router.push(`/posts/${created.id}/edit`)
    }
  } catch (e) {
    saveError.value = typeof e === 'string' ? e : (e?.message || 'Có lỗi xảy ra')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.header-actions { display: flex; gap: 8px; align-items: center; }

.form-layout { display: flex; gap: 20px; align-items: flex-start; }
.form-main   { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 16px; }
.form-side   { width: 280px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px; }

.form-section  { padding: 20px; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.form-row      { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

/* Toggle */
.toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; font-size: 13px; cursor: pointer; }
.toggle { width: 36px; height: 20px; border-radius: 10px; background: #D1D5DB; position: relative; transition: background .2s; flex-shrink: 0; }
.toggle.on { background: var(--brand); }
.toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; border-radius: 50%; background: #fff; transition: transform .2s; }
.toggle.on::after { transform: translateX(16px); }

.error-box { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; }

.cover-row { display: flex; gap: 18px; align-items: flex-start; flex-wrap: wrap; }
.cover-preview {
  width: 240px; height: 150px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid var(--border);
}
.cover-preview img { width: 100%; height: 100%; object-fit: cover; }
.cover-fields { flex: 1; min-width: 260px; }
.upload-row { display: flex; gap: 8px; flex-wrap: wrap; }
textarea.form-input { resize: vertical; font-family: inherit; }

@media (max-width: 900px) {
  .form-layout { flex-direction: column; }
  .form-side { width: 100%; }
  .form-row  { grid-template-columns: 1fr; }
}
</style>
