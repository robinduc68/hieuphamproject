/**
 * v-typewriter
 * ------------
 * Khi phần tử cuộn vào vùng nhìn thấy, chữ sẽ xuất hiện kiểu "gõ máy" (nhanh),
 * ký tự một. Tự nhận diện các text node nên giữ nguyên định dạng inline
 * (<strong>, <em>, <br>, v.v.). Chỉ chạy 1 lần / phần tử.
 *
 * Cách dùng:  <h2 v-typewriter>Tiêu đề</h2>
 * Tuỳ chỉnh tốc độ (ms / ký tự):  <h2 v-typewriter="14">
 */

const DEFAULT_SPEED = 16 // ms / ký tự — nhanh hơn gõ máy thường
const PREPARED_FLAG = 'twPrepared'

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

function escapeChar(ch) {
  if (ch === '<') return '&lt;'
  if (ch === '>') return '&gt;'
  if (ch === '&') return '&amp;'
  return ch
}

/** Tách mọi text node trong el thành các <span class="tw-char"> */
function splitChars(el) {
  if (el.dataset[PREPARED_FLAG]) return
  el.dataset[PREPARED_FLAG] = '1'

  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT)
  const textNodes = []
  let node
  while ((node = walker.nextNode())) textNodes.push(node)

  textNodes.forEach((tn) => {
    const text = tn.nodeValue
    if (!text || !text.length) return
      const frag = document.createDocumentFragment()
      for (const ch of text) {
        const span = document.createElement('span')
        span.className = 'tw-char'
        // Dấu cách giữ nguyên là space bình thường (có thể wrap) — KHÔNG dùng
        // &nbsp;, nếu không text sẽ thành 1 dòng dài tràn ra ngoài card.
        span.innerHTML = escapeChar(ch)
        frag.appendChild(span)
      }
    tn.parentNode.replaceChild(frag, tn)
  })
}

function run(el, speed) {
  const spans = el.querySelectorAll('.tw-char')
  let i = 0
  const tick = () => {
    if (i >= spans.length) {
      el.classList.add('tw-done')
      return
    }
    spans[i].classList.add('tw-show')
    i++
    setTimeout(tick, speed)
  }
  tick()
}

export const vTypewriter = {
  mounted(el, binding) {
    // Người dùng tuỳ chỉnh giảm động → giữ nguyên text, không chạy hiệu ứng.
    if (prefersReducedMotion()) return

    const speed = Number(binding.value) > 0 ? Number(binding.value) : DEFAULT_SPEED
    splitChars(el)

    // Không hỗ trợ IntersectionObserver → chạy luôn.
    if (!('IntersectionObserver' in window)) {
      run(el, speed)
      return
    }

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            io.unobserve(el)
            io.disconnect()
            run(el, speed)
          }
        })
      },
      { threshold: 0.25 }
    )
    io.observe(el)
  },
}
