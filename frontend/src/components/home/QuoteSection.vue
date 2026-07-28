<template>
  <section class="quote-section" ref="sectionEl">
    <!-- Cột trái -->
    <div class="col col-left">
      <img src="/quote-1.png" alt="Khung dệt lụa" class="img img-1" />
      <img src="/quote-2.jpg" alt="Người phụ nữ guồng tơ" class="img img-2" />
    </div>

    <!-- Cột giữa -->
    <div class="col col-center">
      <div class="center-inner" ref="centerInner">
        <p class="quote-line cream">Hà Hoạt Silk hiểu rằng,</p>
        <p class="quote-line cream">bộ đồ "đẹp" nhất không phải</p>
        <p class="quote-line cream">những gì chạy theo số đông, mà là</p>
        <p class="quote-line gold"><em><strong>lựa chọn phù hợp nhất,</strong></em></p>
        <p class="quote-line gold"><em><strong>mang câu chuyện của riêng bạn.</strong></em></p>
        <p class="quote-line cream spacer-top">Để Hà Hoạt Silk giúp bạn</p>
        <p class="quote-line cream">
          <em class="gold"><strong>tự tay</strong></em> tạo nên kiệt tác
          <em class="gold"><strong>độc bản.</strong></em>
        </p>

        <div class="quote-cta">
          <a href="#products" class="btn btn-solid">Khám phá sản phẩm</a>
          <a href="#contact" class="btn btn-outline">Liên hệ hỗ trợ</a>
        </div>
      </div>
    </div>

    <!-- Cột phải -->
    <div class="col col-right">
      <img src="/quote-3.png" alt="Xưởng nhuộm tơ" class="img img-3" />
      <img src="/quote-4.jpg" alt="Lọ gốm nhuộm" class="img img-4" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

/* Pin section ~3 viewport. Lúc đầu: chữ mờ/blur, ảnh trôi dưới (ẩn).
   Scroll: chữ dần hết mờ → rõ, ảnh trôi lên đúng chỗ, CTA hiện cuối. */
const sectionEl = ref(null)
const centerInner = ref(null)
let ctx = null

/* Khoảng cách từ vị trí căn giữa lên sát mép trên của cột giữa.
   Dùng làm điểm bắt đầu của khối chữ; scroll xuống thì y → 0 (về giữa). */
function topOffset() {
  const inner = centerInner.value
  if (!inner) return 0
  const col = inner.parentElement
  return Math.max(0, (col.clientHeight - inner.offsetHeight) / 2)
}

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

/* Chia từng ký tự thành <span class="qchar"> (giữ <em>/<strong>/màu vàng),
   whitespace giữ nguyên để text vẫn xuống dòng tự nhiên. */
function splitChars(el) {
  Array.from(el.childNodes).forEach(node => {
    if (node.nodeType === Node.TEXT_NODE) {
      const frag = document.createDocumentFragment()
      for (const ch of node.textContent) {
        if (/\s/.test(ch)) {
          frag.appendChild(document.createTextNode(ch))
        } else {
          const span = document.createElement('span')
          span.className = 'qchar'
          span.textContent = ch
          frag.appendChild(span)
        }
      }
      node.replaceWith(frag)
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      splitChars(node)
    }
  })
}

onMounted(() => {
  if (prefersReducedMotion()) return
  if (window.innerWidth <= 700) return   // mobile: hiển thị thường, không pin

  ctx = gsap.context(() => {
    // chia ký tự trước khi tạo timeline
    sectionEl.value.querySelectorAll('.quote-line').forEach(splitChars)

    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: sectionEl.value,
        start: 'top top',
        end: '+=84%',         // scroll gấp rưỡi (56%→84%)
        pin: true,
        scrub: 1,
        invalidateOnRefresh: true,   // tính lại topOffset khi resize/ảnh load xong
      },
    })

    // Chữ: mờ (opacity .2) → rõ TỪNG KÝ TỰ, sớm – rút ngắn stagger/duration để text rõ hết trong ~1/3 đầu
    tl.from('.qchar', { opacity: 0.2, duration: 0.22, stagger: 0.005 }, 0)
    // Khối chữ + CTA: bắt đầu sát mép trên → trôi xuống giữa cùng lúc ảnh hiện lên
    tl.from('.center-inner', { y: () => -topOffset(), duration: 0.9 }, 1.3)
    // Hình: hiện muộn hơn (sau khi chữ gần rõ hết)
    tl.from('.img', { y: 240, opacity: 0, duration: 0.5, stagger: 0.08 }, 1.5)
    // CTA cuối
    tl.from('.quote-cta', { opacity: 0, y: 18, duration: 0.5 })

    /* Nền (lớp chung) xám→maroon, NHANH (~1/3 đầu scroll) giống CollectionsGrid.
       Dùng 'to' (không fromTo) để khi chưa tới range không ép giá trị. */
    const pageBg = document.querySelector('[data-page-bg]')
    tl.to(pageBg, { backgroundColor: '#6E1F31', duration: 1.0 }, 0)

    ScrollTrigger.refresh()
    // Ảnh load xong có thể đổi layout → tính lại trigger.
    window.addEventListener('load', ScrollTrigger.refresh)
  }, sectionEl.value)
})

onUnmounted(() => {
  if (typeof window !== 'undefined') window.removeEventListener('load', ScrollTrigger.refresh)
  ctx && ctx.revert()
})
</script>

<style scoped>
.quote-section {
  --bg-maroon: #6E1F31;
  --text-cream: #F5F0E8;
  --accent-gold: #E8D5A8;

  background: var(--bg-maroon);
  min-height: 100vh;
  padding: 56px 60px;
  display: grid;
  grid-template-columns: 1fr 1.4fr 1fr;
  align-items: stretch;
  gap: 8px;
  overflow: hidden;
}
@media (min-width: 701px) {
  .quote-section { background: transparent; }   /* hiện lớp nền chung đổi màu */
}

.col {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.img {
  display: block;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
}

/* Cột trái - so le bậc thang */
.col-left { align-items: flex-end; }
.img-1 {
  width: 215px;
  aspect-ratio: 4 / 3;
  margin-top: 20px;
}
.img-2 {
  width: 325px;
  aspect-ratio: 3 / 4;
  align-self: flex-start;
  margin-bottom: -80px;
  margin-right: -30px;
}

/* Cột phải - đối xứng */
.col-right { align-items: flex-start; }
.img-3 {
  width: 260px;
  aspect-ratio: 3 / 4;
  margin-top: -80px;
}
.img-4 {
  width: 215px;
  aspect-ratio: 3 / 4;
  align-self: flex-end;
  margin-bottom: -20px;
  margin-left: -30px;
}

/* Cột giữa – khối chữ căn giữa dọc, lúc đầu bị GSAP đẩy lên sát mép trên */
.col-center {
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 0 8px;
}
.center-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  will-change: transform;
}

.quote-line {
  font-family: var(--font-display, 'Playfair Display', serif);
  font-size: clamp(24px, 2.4vw, 38px);
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 0.3px;
  margin: 0;
}
.quote-line.cream { color: var(--text-cream); }
.quote-line.gold,
.quote-line .gold { color: var(--accent-gold); }
.quote-line em { font-style: italic; }
.quote-line strong { font-weight: 600; }
.spacer-top { margin-top: 32px; }

.quote-cta {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 18px;
  margin-top: 40px;
}
.btn {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 999px;
  font-family: var(--font-body, inherit);
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease, background 0.2s ease, color 0.2s ease;
}
.btn-solid {
  background: var(--text-cream);
  color: var(--bg-maroon);
}
.btn-solid:hover { transform: translateY(-2px); opacity: 0.92; }
.btn-outline {
  background: transparent;
  color: var(--text-cream);
  border: 1px solid rgba(245, 240, 232, 0.7);
}
.btn-outline:hover {
  background: rgba(245, 240, 232, 0.12);
  transform: translateY(-2px);
}

/* Tablet */
@media (max-width: 1024px) {
  .quote-section {
    grid-template-columns: 1fr 1.2fr;
    min-height: 100vh;
  }
  .col-right { display: none; }
}

/* Mobile */
@media (max-width: 700px) {
  .quote-section {
    grid-template-columns: 1fr;
    padding: 60px 24px;
    gap: 24px;
  }
  .col-left,
  .col-right { display: none; }
  .quote-line { font-size: clamp(20px, 6vw, 28px); }
  .quote-cta { flex-direction: column; align-items: center; }
  .btn { width: 100%; max-width: 320px; text-align: center; }
}
</style>
