<template>
  <div class="rte" :class="{ focused }">
    <div class="rte-toolbar">
      <button
        v-for="b in blockButtons" :key="b.tag"
        type="button" class="rte-btn" :class="{ active: currentBlock === b.tag }"
        :title="b.title" @mousedown.prevent="setBlock(b.tag)"
      >{{ b.label }}</button>

      <span class="rte-sep" />

      <button type="button" class="rte-btn bold"   :class="{ active: state.bold }"      title="Đậm (Ctrl+B)"     @mousedown.prevent="exec('bold')">B</button>
      <button type="button" class="rte-btn italic" :class="{ active: state.italic }"    title="Nghiêng (Ctrl+I)" @mousedown.prevent="exec('italic')">I</button>
      <button type="button" class="rte-btn under"  :class="{ active: state.underline }" title="Gạch chân (Ctrl+U)" @mousedown.prevent="exec('underline')">U</button>

      <span class="rte-sep" />

      <button type="button" class="rte-btn" title="Danh sách chấm đầu dòng" @mousedown.prevent="exec('insertUnorderedList')">• List</button>
      <button type="button" class="rte-btn" title="Danh sách đánh số"       @mousedown.prevent="exec('insertOrderedList')">1. List</button>
      <button type="button" class="rte-btn" title="Chèn liên kết"           @mousedown.prevent="insertLink">🔗</button>
      <button type="button" class="rte-btn" title="Chèn ảnh vào nội dung"   @mousedown.prevent="pickImage" :disabled="uploading">
        {{ uploading ? 'Đang tải ảnh…' : '🖼 Ảnh' }}
      </button>

      <span class="rte-sep" />

      <button type="button" class="rte-btn" title="Xoá định dạng" @mousedown.prevent="clearFormat">Xoá ĐD</button>

      <input ref="imgInput" type="file" accept="image/*" style="display:none" @change="onImageSelected" />
    </div>

    <!-- Thanh chỉnh ảnh: hiện khi bấm vào một ảnh trong nội dung -->
    <div v-if="selectedImage" class="rte-imgbar">
      <span class="rte-imgbar-label">Cỡ ảnh:</span>
      <button
        v-for="s in IMAGE_SIZES" :key="s.cls"
        type="button" class="rte-btn"
        :class="{ active: selectedSizeClass === s.cls }"
        @mousedown.prevent="setImageSize(s.cls)"
      >{{ s.label }}</button>
      <span class="rte-sep" />
      <button type="button" class="rte-btn" title="Căn trái"  :class="{ active: selectedAlign === 'left' }"   @mousedown.prevent="setImageAlign('left')">⇤</button>
      <button type="button" class="rte-btn" title="Căn giữa"  :class="{ active: selectedAlign === 'center' }" @mousedown.prevent="setImageAlign('center')">↔</button>
      <button type="button" class="rte-btn" title="Căn phải"  :class="{ active: selectedAlign === 'right' }"  @mousedown.prevent="setImageAlign('right')">⇥</button>
      <span class="rte-sep" />
      <button type="button" class="rte-btn danger" @mousedown.prevent="removeImage">Xoá ảnh</button>
    </div>

    <div
      ref="editor"
      class="rte-body"
      contenteditable="true"
      :data-placeholder="placeholder"
      :style="{ minHeight: minHeight + 'px' }"
      @input="onInput"
      @paste="onPaste"
      @keyup="syncState"
      @mouseup="syncState"
      @click="onBodyClick"
      @focus="focused = true"
      @blur="focused = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { uploadsApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Nhập nội dung…' },
  minHeight: { type: Number, default: 140 },
})
const emit = defineEmits(['update:modelValue'])

const toast    = useToastStore()
const editor   = ref(null)
const imgInput = ref(null)
const focused  = ref(false)
const uploading = ref(false)
const currentBlock = ref('p')
const state = ref({ bold: false, italic: false, underline: false })

const blockButtons = [
  { tag: 'p',  label: 'Đoạn', title: 'Đoạn văn thường' },
  { tag: 'h1', label: 'H1',   title: 'Tiêu đề lớn' },
  { tag: 'h2', label: 'H2',   title: 'Tiêu đề vừa' },
  { tag: 'h3', label: 'H3',   title: 'Tiêu đề nhỏ' },
]

/** Nội dung cũ lưu dạng text thuần → chuyển sang HTML để hiện đúng đoạn. */
function toHtml(value) {
  const v = (value ?? '').trim()
  if (!v) return ''
  if (/<[a-z][\s\S]*>/i.test(v)) return v
  return v
    .split(/\n{2,}/)
    .map(par => `<p>${escapeHtml(par).replace(/\n/g, '<br>')}</p>`)
    .join('')
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

/** Editor rỗng vẫn để lại <br>/<p></p> — quy về chuỗi rỗng để backend nhận null. */
function normalize(html) {
  const stripped = html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
  const hasMedia = /<(img|hr|iframe)\b/i.test(html)
  return stripped || hasMedia ? html : ''
}

/** HTML sạch để lưu: bỏ dấu chọn ảnh (chỉ phục vụ lúc soạn, không lưu vào DB). */
function cleanHtml() {
  const clone = editor.value.cloneNode(true)
  clone.querySelectorAll('[data-rte-selected]').forEach(el => el.removeAttribute('data-rte-selected'))
  return normalize(clone.innerHTML)
}

let lastEmitted = null

function onInput() {
  const html = cleanHtml()
  lastEmitted = html
  emit('update:modelValue', html)
  syncState()
}

onMounted(() => {
  editor.value.innerHTML = toHtml(props.modelValue)
})

// Chỉ ghi lại DOM khi giá trị đến từ bên ngoài (VD: nạp form khi sửa sản phẩm),
// nếu không con trỏ sẽ nhảy về đầu mỗi lần gõ.
watch(() => props.modelValue, (val) => {
  if (val === lastEmitted) return
  if (!editor.value) return
  editor.value.innerHTML = toHtml(val)
})

function exec(cmd, arg = null) {
  editor.value.focus()
  document.execCommand(cmd, false, arg)
  onInput()
}

function setBlock(tag) {
  exec('formatBlock', `<${tag}>`)
}

function syncState() {
  try {
    state.value = {
      bold:      document.queryCommandState('bold'),
      italic:    document.queryCommandState('italic'),
      underline: document.queryCommandState('underline'),
    }
    const block = (document.queryCommandValue('formatBlock') || 'p').toLowerCase()
    currentBlock.value = ['h1', 'h2', 'h3'].includes(block) ? block : 'p'
  } catch { /* trình duyệt không hỗ trợ queryCommandState — bỏ qua */ }
}

function insertLink() {
  const url = prompt('Nhập đường dẫn (URL):', 'https://')
  if (url) exec('createLink', url)
}

function clearFormat() {
  exec('removeFormat')
  setBlock('p')
}

function pickImage() {
  imgInput.value.click()
}

async function onImageSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const { url } = await uploadsApi.image(fd)
    // Mặc định cỡ vừa (50%) — ảnh gốc thường rất to nếu để nguyên
    exec('insertHTML', `<img src="${url}" alt="" class="rt-img-50">`)
    toast.success('Đã chèn ảnh — bấm vào ảnh để đổi cỡ')
  } catch (err) {
    toast.error('Lỗi upload ảnh: ' + err)
  } finally {
    uploading.value = false
  }
}

// ── Chỉnh ảnh đã chèn ─────────────────────────────────────────────────────
const IMAGE_SIZES = [
  { cls: 'rt-img-25',  label: 'Nhỏ 25%' },
  { cls: 'rt-img-50',  label: 'Vừa 50%' },
  { cls: 'rt-img-75',  label: 'Lớn 75%' },
  { cls: 'rt-img-100', label: 'Tràn 100%' },
]
const ALIGN_CLASSES = { left: 'rt-img-left', center: 'rt-img-center', right: 'rt-img-right' }

const selectedImage     = ref(null)
const selectedSizeClass = ref('')
const selectedAlign     = ref('center')

function onBodyClick(e) {
  if (e.target.tagName === 'IMG') selectImage(e.target)
  else deselectImage()
}

function selectImage(img) {
  deselectImage()
  selectedImage.value = img
  img.setAttribute('data-rte-selected', '')
  selectedSizeClass.value = IMAGE_SIZES.find(s => img.classList.contains(s.cls))?.cls || 'rt-img-100'
  selectedAlign.value =
    Object.entries(ALIGN_CLASSES).find(([, cls]) => img.classList.contains(cls))?.[0] || 'center'
}

function deselectImage() {
  selectedImage.value?.removeAttribute('data-rte-selected')
  selectedImage.value = null
}

function setImageSize(cls) {
  const img = selectedImage.value
  if (!img) return
  IMAGE_SIZES.forEach(s => img.classList.remove(s.cls))
  img.classList.add(cls)
  selectedSizeClass.value = cls
  onInput()
}

function setImageAlign(align) {
  const img = selectedImage.value
  if (!img) return
  Object.values(ALIGN_CLASSES).forEach(cls => img.classList.remove(cls))
  img.classList.add(ALIGN_CLASSES[align])
  selectedAlign.value = align
  onInput()
}

function removeImage() {
  const img = selectedImage.value
  if (!img) return
  selectedImage.value = null
  img.remove()
  onInput()
}

// Dán từ Word/web mang theo style rác → dán dạng text thuần, giữ xuống dòng.
function onPaste(e) {
  e.preventDefault()
  const text = e.clipboardData.getData('text/plain')
  const html = escapeHtml(text).replace(/\n/g, '<br>')
  document.execCommand('insertHTML', false, html)
  onInput()
}
</script>

<style scoped>
.rte {
  border: 1px solid var(--border);
  border-radius: 6px;
  background: #fff;
  overflow: hidden;
  transition: border-color var(--trans);
}
.rte.focused { border-color: var(--brand); }

.rte-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  padding: 6px 8px;
  border-bottom: 1px solid var(--border);
  background: #FAFBFC;
}
.rte-btn {
  min-width: 30px;
  height: 28px;
  padding: 0 8px;
  border: 1px solid transparent;
  border-radius: 5px;
  background: none;
  font-size: 12px;
  color: var(--text-2);
  transition: all var(--trans);
}
.rte-btn:hover:not(:disabled) { background: #EEF1F4; color: var(--text); }
.rte-btn.active { background: #fff; border-color: var(--border); color: var(--brand); font-weight: 600; }
.rte-btn:disabled { opacity: .5; cursor: default; }
.rte-btn.bold   { font-weight: 700; }
.rte-btn.italic { font-style: italic; }
.rte-btn.under  { text-decoration: underline; }
.rte-sep { width: 1px; height: 18px; background: var(--border); margin: 0 4px; }

.rte-body {
  padding: 12px 14px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--text);
  outline: none;
  overflow-y: auto;
  max-height: 420px;
}
.rte-body:empty::before {
  content: attr(data-placeholder);
  color: #9CA3AF;
}
.rte-body :deep(h1) { font-size: 22px; font-weight: 700; margin: 12px 0 8px; }
.rte-body :deep(h2) { font-size: 18px; font-weight: 700; margin: 12px 0 8px; }
.rte-body :deep(h3) { font-size: 15px; font-weight: 700; margin: 10px 0 6px; }
.rte-body :deep(p)  { margin: 0 0 8px; }
.rte-body :deep(ul), .rte-body :deep(ol) { margin: 0 0 8px; padding-left: 22px; }
.rte-body :deep(img) {
  max-width: 100%; height: auto; border-radius: 6px;
  margin: 8px 0; cursor: pointer; display: block;
}
/* Cỡ ảnh — khớp với CSS ngoài website (frontend/src/assets/rich-text.css) */
.rte-body :deep(img.rt-img-25)  { width: 25%; }
.rte-body :deep(img.rt-img-50)  { width: 50%; }
.rte-body :deep(img.rt-img-75)  { width: 75%; }
.rte-body :deep(img.rt-img-100) { width: 100%; }
.rte-body :deep(img.rt-img-left)   { margin-right: auto; }
.rte-body :deep(img.rt-img-center) { margin-left: auto; margin-right: auto; }
.rte-body :deep(img.rt-img-right)  { margin-left: auto; }
.rte-body :deep(img[data-rte-selected]) { outline: 2px solid var(--brand); outline-offset: 2px; }

.rte-imgbar {
  display: flex; align-items: center; flex-wrap: wrap; gap: 4px;
  padding: 6px 8px; background: #F4F7FB; border-bottom: 1px solid var(--border);
}
.rte-imgbar-label { font-size: 12px; color: var(--text-2); margin-right: 4px; }
.rte-btn.danger { color: #DC2626; }
.rte-btn.danger:hover { background: #FEF2F2; }
.rte-body :deep(a) { color: var(--blue); text-decoration: underline; }

@media (max-width: 640px) {
  .rte-toolbar { flex-wrap: wrap; row-gap: 6px; }
}
</style>
