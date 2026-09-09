<template>
  <section class="features-section" :class="{ 'bg-anim': bgAnim }" ref="sectionEl">
    <div class="features-inner">
      <!-- Left title -->
      <div class="features-title">
        <p class="title-script">Đặc quyền</p>
        <p class="title-regular">của lựa chọn</p>
        <p class="title-italic">May đo cá nhân hóa</p>
      </div>

      <!-- Right: 4 cards -->
      <div class="features-cards">
        <div v-for="feat in features" :key="feat.title" class="feat-card">
          <img class="feat-icon" :src="feat.icon" :alt="feat.title.replace('\n',' ')" />
          <h3 class="feat-title">{{ feat.title }}</h3>
          <p class="feat-desc">{{ feat.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const sectionEl = ref(null)
/* true khi timeline đổi nền thật sự chạy → mới cho section trong suốt.
   Nếu không (mobile / prefers-reduced-motion) giữ nền xám đặc. */
const bgAnim = ref(false)
let ctx = null

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

const features = [
  {
    title: 'Thiết kế riêng\nđộc nhất',
    desc: 'Không tồn tại sản phẩm thứ hai hoàn toàn giống "tác phẩm" bạn tạo nên.',
    icon: '/2.png',   // áo dài + vân tay: cá nhân hóa
  },
  {
    title: 'Vừa vặn\ntừng đường nét',
    desc: 'Tùy chọn may theo bảng kích thước sản phẩm hoặc số đo cá nhân, miễn sao phù hợp với bạn.',
    icon: '/4.png',   // ma-nơ-canh + thước dây: đo may chuẩn form
  },
  {
    title: 'Trọn vẹn\ntrải nghiệm',
    desc: 'Trọn gói mọi trải nghiệm với lụa tơ tằm, từ chọn vải, chọn họa tiết, chọn cách may.',
    icon: '/5.png',   // kiểm định an toàn, không hóa chất độc hại
  },
  {
    title: 'Hỗ trợ\nlâu dài',
    desc: 'Đồng hành cùng bạn chăm sóc, bảo quản sản phẩm bền đẹp.',
    icon: '/3.png',   // khăn lụa + khiên trái tim: bảo hành / chăm sóc
  },
]

/* KHÔNG pin. Chạy đúng trong đoạn section trôi từ đáy viewport lên mép trên
   (start 'top bottom' = ngay khi QuoteSection nhả pin, end 'top top').
   Trước đây pin + start 'top top' nên suốt 100vh đó nội dung vẫn opacity 0
   và nền vẫn maroon → lộ ra một khoảng trống. */
onMounted(() => {
  if (prefersReducedMotion()) return
  if (window.innerWidth <= 700) return

  bgAnim.value = true
  ctx = gsap.context(() => {
    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: sectionEl.value,
        start: 'top bottom',
        end: 'top top',
        scrub: 1,
      },
    })
    const pageBg = document.querySelector('[data-page-bg]')
    /* Thứ tự quan trọng: chữ cream của QuoteSection phải trôi hết đã rồi mới đổi nền
       (cream trên xám = chìm), rồi mới fade nội dung tối của section này lên. */
    tl.to(pageBg, { backgroundColor: '#DEDEDE', duration: 0.35 }, 0.45)
      .from('.features-inner', { opacity: 0, y: 40, duration: 0.45 }, 0.55)
  }, sectionEl.value)
})

onUnmounted(() => {
  if (ctx) ctx.revert()
})
</script>

<style scoped>
.features-section {
  background: #DEDEDE;
  padding: var(--section-y) var(--page-x);
}
@media (min-width: 701px) {
  .features-section.bg-anim {
    background: transparent;    /* hiện lớp nền chung đổi màu */
  }
  .features-section {
    min-height: 100vh;          /* to ra – đầy viewport khi pin đổi màu */
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.features-inner {
  width: 100%;
  max-width: 1540px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 260px 1fr;
  align-items: center;
  gap: 56px;
}

/* Title block */
.features-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-script {
  font-family: var(--font-script);
  font-size: 68px;
  white-space: nowrap;
  color: rgb(104, 25, 39);
  line-height: 1.05;
}

.title-regular {
  font-family: var(--font-body);
  font-size: 32px;
  color: #000000;
  font-weight: 400;
  margin-top: 2px;
}

.title-italic {
  font-family: var(--font-display);
  font-size: 34px;
  font-style: italic;
  color: rgb(104, 25, 39);
  font-weight: 600;
  margin-top: 2px;
  line-height: 1.2;
}

/* Cards */
.features-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.feat-card {
  background: var(--bg-white);
  border-radius: var(--radius);
  padding: 42px 27px 36px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: box-shadow var(--transition);
}
.feat-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,.08); }

.feat-icon {
  width: 96px;
  height: 96px;
  object-fit: contain;
  transition: transform var(--transition);
}
.feat-card:hover .feat-icon { transform: scale(1.06); }

.feat-title {
  font-family: 'Philosopher', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #681927;
  line-height: 1.45;
  white-space: pre-line;
}

.feat-desc {
  font-size: 14px;
  color: #000000;
  line-height: 1.75;
  font-weight: 400;
}

@media (max-width: 1024px) {
  .features-cards { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 900px) {
  .features-inner { grid-template-columns: 1fr; gap: 28px; }
}
@media (max-width: 560px) {
  .features-cards { grid-template-columns: 1fr; gap: 14px; }
}
</style>
