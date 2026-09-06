/**
 * Nội dung sản phẩm (mô tả, chất liệu…) được nhập bằng trình soạn thảo trong
 * trang admin nên có thể chứa HTML: h1/h2, in đậm, in nghiêng, danh sách, ảnh.
 * Dữ liệu cũ vẫn là text thuần → tự chuyển sang đoạn văn.
 *
 * Vẫn lọc HTML trước khi render: tài khoản admin bị chiếm quyền không được phép
 * nhúng <script>/onclick vào trang khách.
 */

const ALLOWED_TAGS = new Set([
  'P', 'BR', 'DIV', 'SPAN',
  'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
  'B', 'STRONG', 'I', 'EM', 'U', 'S', 'SMALL', 'SUB', 'SUP',
  'UL', 'OL', 'LI', 'BLOCKQUOTE', 'HR',
  'A', 'IMG', 'FIGURE', 'FIGCAPTION',
  'TABLE', 'THEAD', 'TBODY', 'TR', 'TH', 'TD',
])

const ALLOWED_ATTRS = {
  A:   ['href', 'title', 'target', 'rel'],
  IMG: ['src', 'alt', 'title', 'width', 'height', 'class'],
}

// Chỉ nhận class cỡ/căn ảnh do trình soạn thảo admin đặt — class lạ bị bỏ,
// tránh việc nội dung nhúng ăn theo class của giao diện.
const ALLOWED_IMG_CLASSES = new Set([
  'rt-img-25', 'rt-img-50', 'rt-img-75', 'rt-img-100',
  'rt-img-left', 'rt-img-center', 'rt-img-right',
])

const SAFE_URL = /^(https?:|mailto:|tel:|\/|#)/i

/** Chuỗi có phải HTML hay chỉ là text thuần. */
export function isHtml(value) {
  return /<[a-z][\s\S]*>/i.test(value ?? '')
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

/** Text thuần → các thẻ <p>, giữ nguyên ngắt dòng. */
export function plainToHtml(value) {
  const v = (value ?? '').trim()
  if (!v) return ''
  return v
    .split(/\n{2,}/)
    .map(par => `<p>${escapeHtml(par).replace(/\n/g, '<br>')}</p>`)
    .join('')
}

function cleanElement(el) {
  for (const child of [...el.children]) {
    if (!ALLOWED_TAGS.has(child.tagName)) {
      // Bỏ thẻ nhưng giữ lại nội dung bên trong (trừ script/style)
      if (child.tagName === 'SCRIPT' || child.tagName === 'STYLE') {
        child.remove()
      } else {
        cleanElement(child)
        child.replaceWith(...child.childNodes)
      }
      continue
    }

    const allowed = ALLOWED_ATTRS[child.tagName] ?? []
    for (const attr of [...child.attributes]) {
      const name = attr.name.toLowerCase()
      if (!allowed.includes(name)) {
        child.removeAttribute(attr.name)
        continue
      }
      if ((name === 'href' || name === 'src') && !SAFE_URL.test(attr.value.trim())) {
        child.removeAttribute(attr.name)
        continue
      }
      if (name === 'class') {
        const kept = attr.value.split(/\s+/).filter(c => ALLOWED_IMG_CLASSES.has(c))
        if (kept.length) child.setAttribute('class', kept.join(' '))
        else child.removeAttribute('class')
      }
    }
    if (child.tagName === 'A' && child.getAttribute('target') === '_blank') {
      child.setAttribute('rel', 'noopener noreferrer')
    }
    cleanElement(child)
  }
}

/** HTML đã lọc, sẵn sàng dùng với v-html. */
export function sanitizeHtml(value) {
  const raw = value ?? ''
  if (!raw) return ''
  const doc = new DOMParser().parseFromString(`<body>${raw}</body>`, 'text/html')
  cleanElement(doc.body)
  return doc.body.innerHTML
}

/** Nội dung bất kỳ (HTML hoặc text cũ) → HTML an toàn để render. */
export function renderRichText(value) {
  const v = (value ?? '').trim()
  if (!v) return ''
  return isHtml(v) ? sanitizeHtml(v) : plainToHtml(v)
}

/** Bản rút gọn không thẻ — dùng cho meta description, tooltip… */
export function richTextToPlain(value) {
  const html = renderRichText(value)
  if (!html) return ''
  const doc = new DOMParser().parseFromString(`<body>${html}</body>`, 'text/html')
  return doc.body.textContent.replace(/\s+/g, ' ').trim()
}
