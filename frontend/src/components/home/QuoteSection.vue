<template>
  <section class="quote-section" :class="{ 'bg-anim': bgAnim, 'm-anim': mAnim }" ref="sectionEl">
    <!-- Cột trái -->
    <div class="col col-left">
      <img src="/quote-1.png" alt="Khung dệt lụa" class="img img-1" width="450" height="800" loading="lazy" decoding="async" />
      <img src="/quote-2.jpg" alt="Người phụ nữ guồng tơ" class="img img-2" width="600" height="800" loading="lazy" decoding="async" />
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
      <img src="/quote-3.png" alt="Xưởng nhuộm tơ" class="img img-3" width="800" height="450" loading="lazy" decoding="async" />
      <img src="/quote-4.jpg" alt="Lọ gốm nhuộm" class="img img-4" width="600" height="800" loading="lazy" decoding="async" />
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
/* true khi timeline đổi nền thật sự chạy → mới cho section trong suốt.
   Nếu không (mobile / prefers-reduced-motion) giữ nền maroon đặc. */
const bgAnim = ref(false)
/* true khi hiệu ứng mobile chạy (pin 1 màn hình, ảnh trôi từ dưới lên). */
const mAnim = ref(false)
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

/* Section ngay trước (NewArrivals) – dùng để biết lúc nó nhả pin.
   Khi nó nhả pin, mép trên QuoteSection nằm cách đỉnh viewport đúng bằng
   chiều cao của nó ⇒ đó là điểm bắt đầu của timeline "giao nhau". */
function prevSectionHeight() {
  const prev = document.querySelector('.custom-section')
  const h = prev ? prev.offsetHeight : window.innerHeight
  return Math.min(h, window.innerHeight)
}

onMounted(() => {
  if (prefersReducedMotion()) return

  // chia ký tự trước khi tạo timeline (dùng chung desktop + mobile)
  sectionEl.value.querySelectorAll('.quote-line').forEach(splitChars)

  const mm = gsap.matchMedia(sectionEl.value)   // scope: selector chuỗi chỉ tìm trong section
  ctx = mm
  mm.add('(min-width: 768px)', () => setupDesktop())
  mm.add('(max-width: 767px)', () => setupMobile())

  // Ảnh load xong có thể đổi layout → tính lại trigger.
  window.addEventListener('load', ScrollTrigger.refresh)
})

function setupDesktop() {
  bgAnim.value = true
  const pageBg = document.querySelector('[data-page-bg]')

  /* ---------- 1. GIAO NHAU: NewArrivals → QuoteSection ----------
     KHÔNG pin. Chạy đúng trong đoạn section trôi từ dưới lên mép trên
     (giống cách CollectionsGrid xử lý giao QuoteSection → CollectionsGrid).
     Trong đoạn này: nền xám → maroon ĐỒNG THỜI chữ hiện ra từng ký tự. */
  const BG_DURATION = 1.4
  const entry = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: sectionEl.value,
      start: () => `top ${prevSectionHeight()}px`,
      end: 'top top',
      scrub: 1,
      invalidateOnRefresh: true,
    },
  })

  /* Chữ: MỜ (opacity .5) → RÕ dần từng ký tự (không phải trống rồi hiện ra).
     stagger = nhịp giữa 2 ký tự, duration = thời gian 1 ký tự sáng lên.
     duration < stagger×7 → mỗi lúc chỉ ~7 ký tự đang sáng ⇒ sóng chạy theo ký tự.

     Sóng chữ chia làm 2 đoạn để dài hơn về scroll: một phần chạy trong đoạn
     giao nhau (100vh – cố định theo layout), phần còn lại chạy tiếp trong đoạn pin
     (dài tuỳ ý qua `end`) ⇒ muốn sóng dài hơn thì giảm ENTRY_RATIO + tăng `end`.
     Chia mảng (không dùng chung 1 timeline) để mỗi timeline tự giữ from-state
     của riêng nó – tránh 2 ScrollTrigger tranh nhau ghi cùng giá trị. */
  const chars = gsap.utils.toArray('.qchar', sectionEl.value)
  const ENTRY_RATIO = 0.15                     // % ký tự chạy trong đoạn giao nhau
  const WAVE_DELAY = 0.4                       // chữ bắt đầu muộn hơn nền (~29% đoạn giao nhau)
  const cut = Math.ceil(chars.length * ENTRY_RATIO)
  const CHAR = { opacity: 0.5, duration: 0.12, stagger: 0.014 }
  entry.from(chars.slice(0, cut), { ...CHAR }, WAVE_DELAY)
  /* Nền (lớp chung) xám → maroon. fromTo vì đầu range chắc chắn là #DEDEDE
     (NewArrivals vừa chuyển tới màu này). */
  entry.fromTo(pageBg,
    { backgroundColor: '#DEDEDE' },
    { backgroundColor: '#681927', duration: BG_DURATION }, 0)
  /* Màu chữ: lúc nền còn xám thì tông tối cho dễ đọc, về cream/gold cùng lúc nền xong. */
  entry.from('.quote-line.cream', { color: '#3A1219', duration: BG_DURATION }, 0)
  entry.from('.quote-line.gold, .quote-line .gold', { color: '#7A5A16', duration: BG_DURATION }, 0)

  /* ---------- 2. PIN: ảnh trồi lên, khối chữ về giữa, CTA ---------- */
  const tl = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: sectionEl.value,
      start: 'top top',
      end: '+=245%',   // dài để phần còn lại của sóng chữ chạy đủ (~2 viewport)
      pin: true,
      scrub: 1,
      invalidateOnRefresh: true,   // tính lại topOffset khi resize/ảnh load xong
    },
  })

  // Phần còn lại của sóng chữ – tiếp tục ngay khi section bắt đầu pin
  tl.from(chars.slice(cut), { ...CHAR }, 0)
  /* Khối chữ + CTA: bắt đầu sát mép trên → trôi xuống giữa cùng lúc ảnh trồi lên.
     duration ngắn hơn sóng chữ nhiều → ảnh/khối chữ vẫn xong sau ~1 viewport
     dù pin dài 290% (nếu để 1.2 thì ảnh trôi lên chậm rề). */
  tl.from('.center-inner', { y: () => -topOffset(), duration: 0.85 }, 0)
  /* Hình: KHÔNG fade – luôn opacity 1, nằm sẵn dưới mép section (overflow:hidden che),
     scroll thì trượt thẳng từ dưới lên đúng chỗ.
     y phải > 1 viewport: img-3 có margin-top -80 nên đỉnh nó nằm TRÊN mép section,
     lấy 0.9vh là chưa đủ đẩy khỏi màn → nó lấp ló sẵn từ đầu. +160 cho dư. */
  tl.from('.img', {
    y: () => window.innerHeight + 160,
    duration: 0.85,
    stagger: 0.12,
  }, 0)
  // CTA cuối
  tl.from('.quote-cta', { opacity: 0, y: 18, duration: 0.5 })

  ScrollTrigger.refresh()
  return () => { bgAnim.value = false }
}

/* ---------- MOBILE: giống leeemb.com ----------
   Section cao đúng 1 màn hình, chữ ở giữa. Trượt lên tới đỉnh thì pin:
   chữ sáng dần từng ký tự, 4 ảnh (mờ 50%) trôi từ dưới lên xuyên qua màn
   hình phía sau chữ như parallax, cuối cùng CTA hiện ra rồi nhả pin. */
function setupMobile() {
  mAnim.value = true
  bgAnim.value = true
  // Thanh địa chỉ co/giãn khi cuộn không được làm ScrollTrigger tính lại (giật)
  ScrollTrigger.config({ ignoreMobileResize: true })

  const q = gsap.utils.selector(sectionEl.value)
  const chars = q('.qchar')
  const CHAR = { opacity: 0.25, duration: 0.12, stagger: 0.014 }
  const ENTRY_RATIO = 0.2
  const cut = Math.ceil(chars.length * ENTRY_RATIO)

  /* 1. GIAO NHAU (như desktop): section trôi từ đáy lên tới lúc khối chữ ở giữa
     màn hình → nền chung xám → maroon, chữ tối → cream/gold, vài dòng đầu sáng trước. */
  const BG_DURATION = 1.4
  const pageBg = document.querySelector('[data-page-bg]')
  const entry = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: sectionEl.value,
      start: 'top bottom',
      endTrigger: centerInner.value,
      end: 'center center',
      scrub: 1,
      invalidateOnRefresh: true,
    },
  })
  entry.fromTo(pageBg,
    { backgroundColor: '#DEDEDE' },
    { backgroundColor: '#681927', duration: BG_DURATION }, 0)
  entry.from(q('.quote-line.cream'), { color: '#3A1219', duration: BG_DURATION }, 0)
  entry.from(q('.quote-line.gold, .quote-line .gold'), { color: '#7A5A16', duration: BG_DURATION }, 0)
  entry.from(chars.slice(0, cut), { ...CHAR }, 0.4)

  /* 2. Pin khi khối chữ vào GIỮA màn hình: phần còn lại của chữ + ảnh trôi lên + CTA.
     Section chỉ cao vừa nội dung (không cao 1 màn hình) → nhả pin xong
     khoảng trống dưới CTA ngắn; phần màn hình dư là nền chung maroon. */
  const tl = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: centerInner.value,
      start: 'center center',
      end: '+=200%',
      pin: sectionEl.value,
      scrub: 1,
      anticipatePin: 1,
      invalidateOnRefresh: true,
    },
  })
  const waveLen = (chars.length - cut) * CHAR.stagger + CHAR.duration
  tl.from(chars.slice(cut), { ...CHAR }, 0)
  /* Đỉnh section trên màn hình lúc đang pin (khối chữ ở giữa màn hình) */
  const pinnedTop = () => {
    const ci = centerInner.value.getBoundingClientRect()
    const sec = sectionEl.value.getBoundingClientRect()
    return window.innerHeight / 2 - (ci.top - sec.top + ci.height / 2)
  }
  /* Ảnh: bắt đầu dưới đáy màn hình, trôi qua vị trí đặt sẵn trong CSS rồi
     tiếp tục lên thêm chút (parallax).
     Cho mượt:
     - Ảnh lazy nằm ngoài màn hình → chỉ được tải/giải mã đúng lúc trồi lên ⇒ khựng.
       Mobile tải + decode sẵn từ đầu.
     - Cả 4 ảnh chạy CÙNG quãng (không so le start/duration) với tốc độ đều
       (ease none) → không ảnh nào tăng/giảm tốc đột ngột; khác nhau chỉ ở
       quãng đường nên vẫn có chiều sâu parallax.
     - Quãng dài ~70% sóng chữ → ảnh trôi chậm, xong trước khi chữ sáng hết.
     - force3D: giữ ảnh trên layer GPU suốt (mặc định GSAP trả về 2D lúc tween
       xong → vẽ lại layer ⇒ giật khi ảnh dừng). */
  const IMG_LEN = waveLen * 0.7
  q('.img').forEach((img, i) => {
    img.loading = 'eager'
    img.decode?.().catch(() => {})
    tl.fromTo(img,
      { y: () => window.innerHeight - pinnedTop() - img.offsetTop + 20 },
      { y: () => -(40 + i * 25), duration: IMG_LEN, force3D: true },
      0)
  })
  // CTA chỉ hiện dần tại chỗ (không trượt y) → nút không nhảy
  tl.from(q('.quote-cta'), { opacity: 0, duration: waveLen * 0.25 }, waveLen * 0.8)

  /* Quote trôi khỏi màn hình → trả nền chung về xám. Nếu để maroon, mép giữa
     các section nền xám (toạ độ lẻ px) lộ ra 1 đường đỏ mảnh trên điện thoại. */
  /* Trigger = section kế tiếp (nằm sau pin-spacer nên vị trí đúng); khi nó
     chạm đỉnh màn hình thì Quote đã trôi hết. */
  const nextSection = document.querySelector('.features-section')
  if (nextSection) ScrollTrigger.create({
    trigger: nextSection,
    start: 'top top',
    onEnter: () => gsap.set(pageBg, { backgroundColor: '#DEDEDE' }),
    onLeaveBack: () => gsap.set(pageBg, { backgroundColor: '#681927' }),
  })

  ScrollTrigger.refresh()
  return () => { mAnim.value = false; bgAnim.value = false }
}

onUnmounted(() => {
  if (typeof window !== 'undefined') window.removeEventListener('load', ScrollTrigger.refresh)
  ctx && ctx.revert()
})
</script>

<style scoped>
.quote-section {
  --bg-maroon: #681927;
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
@media (min-width: 768px) {
  .quote-section.bg-anim { background: transparent; }   /* hiện lớp nền chung đổi màu */
}

.col {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.img {
  display: block;
  height: auto;          /* thuộc tính height="…" (chống layout shift) không được đè aspect-ratio */
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

/* ─── MOBILE (< 768px) ───
   Chữ chảy tự nhiên ở giữa, 4 ảnh làng nghề đặt lệch quanh (absolute),
   một số tràn mép / đè nhẹ dưới chữ như design. */
@media (max-width: 767px) {
  .quote-section {
    --accent-gold: var(--cream);
    position: relative;
    display: block;
    min-height: 0;
    padding: 50px 0 48px;
  }

  .col-left,
  .col-right { display: contents; }

  .img {
    position: absolute;
    z-index: 0;
    margin: 0;
    aspect-ratio: auto;
    border-radius: 10px;
    opacity: .5;
    box-shadow: 0 8px 20px rgba(0, 0, 0, .22);
  }
  .img-1 { top: 30px;  left: 27px;   width: 99px;  height: 130px; }
  .img-3 { top: -6px;  right: -10px; width: 117px; height: 194px; }
  .img-2 { top: 240px; left: -12px;  width: 106px; height: 198px; }
  .img-4 { top: 240px; right: 17px;  width: 102px; height: 122px; }

  .col-center {
    position: relative;
    z-index: 1;
    padding: 0 var(--page-x);
  }
  .center-inner {
    display: block;
    max-width: 350px;
    margin: 0 auto;
    text-wrap: pretty;     /* tránh chữ mồ côi cuối đoạn */
  }

  /* 2 dòng đầu giữ nguyên dòng; phần còn lại chảy liền (inline) để xuống dòng như design */
  .quote-line {
    display: inline;
    font-size: 23px;
    line-height: 1.75;
    letter-spacing: 1.2px;
  }
  .quote-line::after { content: ' '; }
  .center-inner > .quote-line:nth-child(-n+2),
  .spacer-top { display: block; }
  .spacer-top { margin-top: 14px; }

  .quote-cta {
    flex-direction: column;
    align-items: center;
    gap: 17px;
    margin-top: 34px;
  }
  .btn {
    width: 180px;
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 12px;
    font-size: 15px;
    font-weight: 400;
  }
  .btn-solid { background: var(--border); color: var(--brand-red); }
  .btn-outline { border-color: rgba(255, 255, 255, .85); color: #FFFFFF; }

  /* Có hiệu ứng (JS bật .m-anim): section cao vừa nội dung, pin khi khối chữ
     ở giữa màn hình; ảnh đặt theo % chiều cao, GSAP đẩy xuống đáy màn hình rồi trôi lên.
     overflow-y visible để ảnh trôi lên từ đáy MÀN HÌNH (không bị cắt ở đáy section);
     trình duyệt không hỗ trợ clip thì giữ hidden ở rule gốc. */
  .quote-section.m-anim {
    background: transparent;    /* hiện lớp nền chung đổi màu */
    overflow-x: clip;
    overflow-y: visible;
    display: flex;
    align-items: flex-start;    /* gap với section trước ~1/3 */
    padding: calc(70px + env(safe-area-inset-top)) 0 96px;   /* dưới CTA ~1/3 trước (287px) */
  }
  .m-anim .col-center { width: 100%; }
  .m-anim .center-inner { will-change: auto; }
  .m-anim .img { will-change: transform; backface-visibility: hidden; }
  .m-anim .img-1 { top: 14%; }
  .m-anim .img-3 { top: 6%; }
  .m-anim .img-2 { top: auto; bottom: 8%; }
  .m-anim .img-4 { top: auto; bottom: 20%; }
}

@media (max-width: 380px) {
  .quote-line { font-size: 21px; letter-spacing: .8px; }
  .img-1 { width: 84px;  height: 112px; }
  .img-3 { width: 96px;  height: 170px; }
  .img-2 { width: 88px;  height: 170px; }
  .img-4 { width: 86px;  height: 104px; }
}
</style>
