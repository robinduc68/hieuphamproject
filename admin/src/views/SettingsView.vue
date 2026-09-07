<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">Nội dung website</div>
        <div class="page-sub">Video trang chủ và các bảng hướng dẫn hiện ngoài web</div>
      </div>
    </div>

    <div v-if="loading" class="card empty-state">Đang tải...</div>

    <template v-else>
      <!-- ── Video nền trang chủ ───────────────────────────────────────── -->
      <div class="card form-section">
        <div class="section-title">Video nền trang chủ</div>
        <p class="form-hint" style="margin-bottom:14px">
          Video chạy tự động, lặp, không tiếng ở ngay đầu trang chủ. Nên dùng MP4 hoặc WEBM,
          tối đa 200MB. Ảnh poster hiện trong lúc video đang tải.
        </p>

        <div class="video-row">
          <div class="video-preview">
            <video v-if="previewable" :src="heroVideo.url" :poster="heroVideo.poster || undefined"
                   muted loop autoplay playsinline />
            <div v-else class="video-empty">
              {{ heroVideo.url ? 'Không xem trước được ở đây — mở trang chủ để kiểm tra' : 'Chưa có video' }}
            </div>
          </div>

          <div class="video-fields">
            <div class="form-group">
              <label class="form-label">Đường dẫn video</label>
              <input v-model="heroVideo.url" class="form-input" placeholder="/videos/hero.webm" />
              <span class="form-hint">Dán URL sẵn có, hoặc bấm “Tải video lên” để chọn file từ máy.</span>
            </div>
            <div class="form-group">
              <label class="form-label">Ảnh poster (tuỳ chọn)</label>
              <input v-model="heroVideo.poster" class="form-input" placeholder="/videos/hero-poster.jpg" />
            </div>

            <div class="upload-row">
              <button class="btn btn-secondary" :disabled="uploading" @click="$refs.videoInput.click()">
                {{ uploading ? `Đang tải lên ${uploadPct}%` : 'Tải video lên' }}
              </button>
              <button class="btn btn-secondary" :disabled="uploading" @click="$refs.posterInput.click()">
                Tải ảnh poster
              </button>
              <input ref="videoInput"  type="file" accept="video/*" style="display:none" @change="onVideoSelected" />
              <input ref="posterInput" type="file" accept="image/*" style="display:none" @change="onPosterSelected" />
            </div>
            <div v-if="uploading" class="progress"><div class="progress-bar" :style="{ width: uploadPct + '%' }" /></div>

            <button class="btn btn-primary" :disabled="saving.hero_video" @click="save('hero_video', heroVideo)">
              {{ saving.hero_video ? 'Đang lưu...' : 'Lưu video trang chủ' }}
            </button>
          </div>
        </div>
      </div>

      <!-- ── Hướng dẫn chọn size ───────────────────────────────────────── -->
      <div class="card form-section">
        <div class="section-title">Bảng “Hướng dẫn chọn size”</div>
        <p class="form-hint" style="margin-bottom:14px">
          Hiện khi khách bấm “Hướng dẫn chọn size” ở trang chi tiết sản phẩm quần áo.
        </p>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Tiêu đề</label>
            <input v-model="sizeGuide.title" class="form-input" placeholder="Hướng Dẫn Chọn Size" />
          </div>
          <div class="form-group">
            <label class="form-label">Ghi chú cuối bảng</label>
            <input v-model="sizeGuide.note" class="form-input" placeholder="* Số đo tính theo cm..." />
          </div>
        </div>
        <TableEditor v-model="sizeGuideTable" />
        <button class="btn btn-primary" style="margin-top:14px" :disabled="saving.size_guide"
                @click="save('size_guide', { ...sizeGuide, ...sizeGuideTable })">
          {{ saving.size_guide ? 'Đang lưu...' : 'Lưu hướng dẫn chọn size' }}
        </button>
      </div>

      <!-- ── Hai hướng dẫn dạng bài viết ───────────────────────────────── -->
      <div v-for="g in articleGuides" :key="g.key" class="card form-section">
        <div class="section-title">{{ g.section }}</div>
        <p class="form-hint" style="margin-bottom:14px">{{ g.hint }}</p>
        <div class="form-group">
          <label class="form-label">Tiêu đề dialog</label>
          <input v-model="g.model.value.title" class="form-input" :placeholder="g.placeholder" />
        </div>
        <div class="form-group">
          <label class="form-label">Nội dung</label>
          <RichTextEditor v-model="g.model.value.content" :min-height="200"
                          placeholder="Soạn nội dung hướng dẫn — có thể thêm tiêu đề, in đậm, danh sách và ảnh..." />
        </div>
        <button class="btn btn-primary" :disabled="saving[g.key]" @click="save(g.key, g.model.value)">
          {{ saving[g.key] ? 'Đang lưu...' : 'Lưu ' + g.section.toLowerCase() }}
        </button>
      </div>

      <!-- ── Định mức may đo ───────────────────────────────────────────── -->
      <div class="card form-section">
        <div class="section-title">Bảng “Định mức may đo”</div>
        <p class="form-hint" style="margin-bottom:14px">
          Hiện khi khách bấm “Định mức may đo” ở trang chi tiết sản phẩm vải (ngay dưới phần chất liệu).
        </p>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Tiêu đề</label>
            <input v-model="fabricGuide.title" class="form-input" placeholder="Định Mức May Đo" />
          </div>
          <div class="form-group">
            <label class="form-label">Ghi chú cuối bảng</label>
            <input v-model="fabricGuide.note" class="form-input" placeholder="* Định mức tham khảo..." />
          </div>
        </div>
        <TableEditor v-model="fabricGuideTable" />
        <button class="btn btn-primary" style="margin-top:14px" :disabled="saving.fabric_tailoring_guide"
                @click="save('fabric_tailoring_guide', { ...fabricGuide, ...fabricGuideTable })">
          {{ saving.fabric_tailoring_guide ? 'Đang lưu...' : 'Lưu định mức may đo' }}
        </button>
      </div>

      <!-- ── Bộ lọc trang vải ──────────────────────────────────────────── -->
      <div class="card form-section">
        <div class="section-title">Bộ lọc trang vải — danh sách họa tiết</div>
        <p class="form-hint" style="margin-bottom:14px">
          Đây là các mục trong ô lọc <strong>HỌA TIẾT</strong> ở trang
          <strong>Lụa Nha Xá thông dụng</strong>, đồng thời là danh sách chọn trong ô
          “Họa tiết” khi thêm/sửa sản phẩm vải. Sửa tên ở đây thì phải mở lại sản phẩm
          chọn tên mới, nếu không sản phẩm sẽ không khớp mục lọc nào.
        </p>

        <div v-if="!fabricPatterns.length" class="empty-state" style="padding:20px;font-size:13px">
          Chưa có họa tiết nào
        </div>

        <div v-for="(p, i) in fabricPatterns" :key="i" class="pattern-row">
          <span class="pattern-num">{{ i + 1 }}</span>
          <input v-model="fabricPatterns[i]" class="form-input" placeholder="VD: Thọ Dơi" />
          <button class="btn btn-icon btn-sm" title="Lên" :disabled="i === 0" @click="movePattern(i, -1)">↑</button>
          <button class="btn btn-icon btn-sm" title="Xuống" :disabled="i === fabricPatterns.length - 1" @click="movePattern(i, 1)">↓</button>
          <button class="btn btn-icon btn-sm" title="Xoá" @click="fabricPatterns.splice(i, 1)">✕</button>
        </div>

        <div style="display:flex;gap:8px;margin-top:14px">
          <button class="btn btn-secondary" @click="fabricPatterns.push('')">+ Thêm họa tiết</button>
          <button class="btn btn-primary" :disabled="saving.fabric_filters" @click="saveFabricFilters">
            {{ saving.fabric_filters ? 'Đang lưu...' : 'Lưu danh sách họa tiết' }}
          </button>
        </div>
      </div>

      <!-- ── Trang "Câu hỏi thường gặp" ────────────────────────────────── -->
      <div class="card form-section">
        <div class="section-title">Trang “Câu hỏi thường gặp”</div>
        <p class="form-hint" style="margin-bottom:14px">
          Toàn bộ nội dung trang <strong>/cau-hoi-thuong-gap</strong>. Câu đầu tiên mặc định
          được mở sẵn ngoài website.
        </p>

        <div class="form-group">
          <label class="form-label">Tiêu đề trang</label>
          <input v-model="faqPage.title" class="form-input" placeholder="CÂU HỎI THƯỜNG GẶP" />
        </div>

        <div v-if="!faqPage.items.length" class="empty-state" style="padding:20px;font-size:13px">
          Chưa có câu hỏi nào
        </div>

        <div v-for="(item, i) in faqPage.items" :key="i" class="faq-row">
          <div class="faq-row-head">
            <span class="faq-row-num">{{ i + 1 }}</span>
            <div class="faq-row-actions">
              <button class="btn btn-icon btn-sm" title="Lên" :disabled="i === 0" @click="moveFaq(i, -1)">↑</button>
              <button class="btn btn-icon btn-sm" title="Xuống" :disabled="i === faqPage.items.length - 1" @click="moveFaq(i, 1)">↓</button>
              <button class="btn btn-icon btn-sm" title="Xoá" @click="faqPage.items.splice(i, 1)">✕</button>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Câu hỏi</label>
            <input v-model="item.question" class="form-input" placeholder="VD: Chính sách đổi trả như thế nào?" />
          </div>
          <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Câu trả lời</label>
            <textarea v-model="item.answer" class="form-input faq-answer" rows="4" placeholder="Nội dung trả lời..." />
          </div>
        </div>

        <div style="display:flex;gap:8px;margin-top:14px">
          <button class="btn btn-secondary" @click="faqPage.items.push({ question: '', answer: '' })">
            + Thêm câu hỏi
          </button>
          <button class="btn btn-primary" :disabled="saving.faq_page" @click="save('faq_page', faqPage)">
            {{ saving.faq_page ? 'Đang lưu...' : 'Lưu câu hỏi thường gặp' }}
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { settingsApi, uploadsApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import TableEditor from '@/components/TableEditor.vue'
import RichTextEditor from '@/components/RichTextEditor.vue'
import { PATTERNS as DEFAULT_PATTERNS } from '@/data/fabricOptions.js'

const toast = useToastStore()

const loading   = ref(true)
const uploading = ref(false)
const uploadPct = ref(0)
const saving    = ref({})

const heroVideo   = ref({ url: '', poster: '' })

// Trang admin chỉ phục vụ được file trong /media (video tải lên) và URL tuyệt đối.
// Đường dẫn kiểu /videos/hero.webm nằm trong app khách nên xem trước ở đây sẽ 404.
const previewable = computed(() => {
  const url = heroVideo.value.url?.trim()
  return !!url && (url.startsWith('/media/') || /^https?:\/\//i.test(url))
})
const sizeGuide   = ref({ title: '', note: '' })
const fabricGuide = ref({ title: '', note: '' })
// Bảng tách riêng khỏi title/note để dùng chung component TableEditor
const sizeGuideTable   = ref({ columns: [], rows: [] })
const fabricGuideTable = ref({ columns: [], rows: [] })

// Hai hướng dẫn dạng bài viết (nội dung HTML soạn bằng trình soạn thảo)
const measureGuide = ref({ title: '', content: '' })
const colorGuide   = ref({ title: '', content: '' })

// Danh sách họa tiết của bộ lọc trang vải
const fabricPatterns = ref([])

function movePattern(i, delta) {
  const j = i + delta
  if (j < 0 || j >= fabricPatterns.value.length) return
  const list = fabricPatterns.value
  ;[list[i], list[j]] = [list[j], list[i]]
}

// Bỏ mục trống và mục trùng trước khi lưu — danh sách này là nguồn cho cả
// bộ lọc ngoài web lẫn ô chọn trong form sản phẩm.
function saveFabricFilters() {
  const cleaned = [...new Set(fabricPatterns.value.map(p => p.trim()).filter(Boolean))]
  fabricPatterns.value = cleaned
  save('fabric_filters', { patterns: cleaned })
}

// Trang "Câu hỏi thường gặp" — toàn bộ nội dung nằm ở một key duy nhất
const faqPage = ref({ title: '', items: [] })

function moveFaq(i, delta) {
  const items = faqPage.value.items
  const j = i + delta
  if (j < 0 || j >= items.length) return
  ;[items[i], items[j]] = [items[j], items[i]]
}

const articleGuides = [
  {
    key: 'measure_guide',
    model: measureGuide,
    section: 'Hướng dẫn lấy số đo & đặt may',
    placeholder: 'Hướng Dẫn Lấy Số Đo & Đặt May',
    hint: 'Hiện khi khách bấm “Hướng dẫn lấy số đo & đặt may” ở trang chi tiết sản phẩm quần áo.',
  },
  {
    key: 'color_guide',
    model: colorGuide,
    section: 'Hướng dẫn chọn màu & đặt may',
    placeholder: 'Hướng Dẫn Chọn Màu & Đặt May',
    hint: 'Hiện khi khách bấm “Hướng dẫn chọn màu & đặt may” ở phần lựa chọn màu sắc.',
  },
]

function splitTable(value, fallbackColumns) {
  const v = value ?? {}
  return {
    meta:  { title: v.title ?? '', note: v.note ?? '' },
    table: { columns: v.columns ?? fallbackColumns, rows: v.rows ?? [] },
  }
}

onMounted(async () => {
  try {
    const data = await settingsApi.list()

    heroVideo.value = { url: data.hero_video?.url ?? '', poster: data.hero_video?.poster ?? '' }

    const size = splitTable(data.size_guide, ['Size', 'Ngực (cm)', 'Eo (cm)', 'Hông (cm)', 'Chiều cao (cm)'])
    sizeGuide.value      = size.meta
    sizeGuideTable.value = size.table

    const fab = splitTable(data.fabric_tailoring_guide, ['Sản phẩm', 'Chiều cao', 'Định mức vải (mét)'])
    fabricGuide.value      = fab.meta
    fabricGuideTable.value = fab.table

    measureGuide.value = {
      title:   data.measure_guide?.title   ?? 'Hướng Dẫn Lấy Số Đo & Đặt May',
      content: data.measure_guide?.content ?? '',
    }
    colorGuide.value = {
      title:   data.color_guide?.title   ?? 'Hướng Dẫn Chọn Màu & Đặt May',
      content: data.color_guide?.content ?? '',
    }

    fabricPatterns.value = Array.isArray(data.fabric_filters?.patterns)
      ? [...data.fabric_filters.patterns]
      : [...DEFAULT_PATTERNS]

    faqPage.value = {
      title: data.faq_page?.title ?? 'CÂU HỎI THƯỜNG GẶP',
      items: (data.faq_page?.items ?? []).map(it => ({
        question: it.question ?? '',
        answer:   it.answer   ?? '',
      })),
    }
  } catch (e) {
    toast.error('Lỗi tải cấu hình: ' + e)
  } finally {
    loading.value = false
  }
})

async function save(key, value) {
  saving.value = { ...saving.value, [key]: true }
  try {
    await settingsApi.save(key, value)
    toast.success('Đã lưu — kiểm tra lại ngoài website')
  } catch (e) {
    toast.error('Lỗi lưu cấu hình: ' + e)
  } finally {
    saving.value = { ...saving.value, [key]: false }
  }
}

async function onVideoSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  uploading.value = true
  uploadPct.value = 0
  try {
    const fd = new FormData()
    fd.append('file', file)
    const { url } = await uploadsApi.video(fd, (p) => {
      if (p.total) uploadPct.value = Math.round((p.loaded / p.total) * 100)
    })
    heroVideo.value.url = url
    toast.success('Tải video xong — nhớ bấm “Lưu video trang chủ”')
  } catch (err) {
    toast.error('Lỗi tải video: ' + err)
  } finally {
    uploading.value = false
  }
}

async function onPosterSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  try {
    const fd = new FormData()
    fd.append('file', file)
    const { url } = await uploadsApi.image(fd)
    heroVideo.value.poster = url
    toast.success('Tải poster xong — nhớ bấm “Lưu video trang chủ”')
  } catch (err) {
    toast.error('Lỗi tải ảnh: ' + err)
  }
}
</script>

<style scoped>
.form-section  { padding: 20px; margin-bottom: 16px; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.form-row      { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.video-row { display: flex; gap: 20px; align-items: flex-start; }
.video-preview {
  width: 300px; flex-shrink: 0; aspect-ratio: 16/9;
  background: #111; border-radius: 8px; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}
.video-preview video { width: 100%; height: 100%; object-fit: cover; }
.video-empty { color: #9CA3AF; font-size: 13px; }
.video-fields { flex: 1; min-width: 0; }

.upload-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }

.faq-row {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 12px;
}
.faq-row-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.faq-row-num { font-size: 12px; font-weight: 600; color: var(--text-2); }
.faq-row-actions { display: flex; gap: 6px; }
.faq-answer { resize: vertical; font-family: inherit; line-height: 1.6; }

.pattern-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.pattern-row .form-input { flex: 1; }
.pattern-num { width: 22px; font-size: 12px; color: var(--text-2); flex-shrink: 0; }

.progress { height: 6px; background: var(--bg); border-radius: 3px; overflow: hidden; margin-bottom: 12px; }
.progress-bar { height: 100%; background: var(--brand); transition: width .2s; }

@media (max-width: 900px) {
  .video-row { flex-direction: column; }
  .video-preview { width: 100%; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
