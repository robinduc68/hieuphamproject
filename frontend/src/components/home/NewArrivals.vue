<template>
  <section class="custom-section" ref="sectionEl">
    <div class="custom-inner">

      <!-- Top: 2-line centered heading -->
      <div class="custom-top">
        <h2 class="custom-heading">THIẾT KẾ TRANG PHỤC ĐỘC BẢN</h2>
        <p class="custom-sub">Trải nghiệm cá nhân hóa trên nền Lụa tơ tằm</p>
      </div>

      <!-- 4 steps – card dọc, 4 cột -->
      <div class="steps">
        <div
          v-for="(step, index) in steps"
          :key="step.num"
          class="step"
          :style="{ marginTop: index * 16 + 'px' }"
        >
          <span class="step-num">{{ step.num }}</span>
          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-desc">{{ step.desc }}</p>
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
let ctx = null

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

const steps = [
  {
    num: '01',
    title: 'Chọn mẫu áo dài, pháp phục',
    desc: 'Lựa chọn mẫu theo sở thích',
  },
  {
    num: '02',
    title: 'Điều chỉnh các tùy chọn',
    desc: 'Cân nhắc các lựa chọn hình thức may, kiểu dáng, phối màu',
  },
  {
    num: '03',
    title: 'Hoàn thiện thiết kế riêng',
    desc: 'Thay đổi mẫu vải nếu có nhu cầu để tạo ra thiết kế độc bản chỉ riêng bạn có.',
  },
  {
    num: '04',
    title: 'Sản phẩm được chế tác',
    desc: 'Hà Hoạt Silk giúp bạn hoàn thiện sản phẩm mang dấu ấn riêng.',
  },
]

/* Pin section ~1.5 viewport. Scroll: nền chuyển dần trắng → #DEDEDE (màu section). */
onMounted(() => {
  if (prefersReducedMotion()) return
  if (window.innerWidth <= 700) return   // mobile: nền #DEDEDE tĩnh, không pin

  const pageBg = document.querySelector('[data-page-bg]')   // lớp nền chung – không lộ đường nối
  ctx = gsap.context(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: sectionEl.value,
        start: 'top top',
        end: '+=90%',          // gấp đôi – thêm thời gian xem
        pin: true,
        scrub: 1,
      },
    })
    // Màu chuyển NHANH (1/3 đầu scroll); phần còn lại giữ nguyên cho xem
    tl.fromTo(pageBg, { backgroundColor: '#FFFFFF' }, { backgroundColor: '#DEDEDE', ease: 'none', duration: 0.3 }, 0)
    tl.fromTo('.step', { backgroundColor: '#F2F2F2' }, { backgroundColor: '#FFFFFF', ease: 'none', duration: 0.3 }, 0)
    tl.to({}, { duration: 0.7 })   // hold – kéo dài pin mà màu đã chuyển xong
  }, sectionEl.value)
})

onUnmounted(() => {
  if (ctx) ctx.revert()
})
</script>

<style scoped>
.custom-section {
  background: #DEDEDE;
  padding: 56px 24px;
  color: rgb(104, 25, 39);
}
@media (min-width: 701px) {
  .custom-section {
    background: transparent;    /* trong suốt – hiện lớp nền chung đổi màu */
    min-height: 80vh;          /* ngắn lại xíu – hiệu ứng chuyển màu nền vẫn giữ */
    display: flex;
    align-items: flex-start;   /* tiêu đề lên đầu – sát FabricShowcase bên trên */
    justify-content: center;
    padding-top: 56px;
  }
}

.custom-inner {
  max-width: none;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 44px;
}

/* Top: centered 2-line heading */
.custom-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
  padding-top: 8px;
}

.custom-heading {
  font-family: 'Philosopher', sans-serif;
  font-size: 46px;
  color: rgb(104, 25, 39);
  line-height: 1.3;
}

.custom-sub {
  font-family: var(--font-script);
  font-size: 46px;
  color: rgb(104, 25, 39);
  line-height: 1.2;
}

/* Steps – card dọc, 4 cột, rộng full */
.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  align-items: start;
}

.step {
  background: #F2F2F2;          /* xám rất nhạt – gần trắng, nổi nhẹ nhàng */
  border-radius: 12px;
  padding: 36px 26px 64px;     /* to chiều dài ra xíu */
  min-height: 380px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .04);   /* shadow nền rất nhẹ – đậm hơn nhiều khi hover */
  transition: transform var(--transition), box-shadow var(--transition);
}
.step:hover {
  transform: scale(1.03);
  box-shadow: 0 14px 36px rgba(104, 25, 39, .18);
  z-index: 2;
}

.step-num {
  font-family: var(--font-script);
  font-size: 108px;            /* ×1.5 */
  line-height: 1;
  /* gradient rõ 100% (đậm) → rõ 5% (mờ dần topo→bottom) */
  background: linear-gradient(180deg, #681927 0%, rgba(104, 25, 39, 0.05) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}

.step-title {
  font-family: 'Philosopher', sans-serif;
  font-size: 36px;             /* ×1.5 */
  color: rgb(104, 25, 39);
  line-height: 1.35;
}

.step-desc {
  font-size: 16px;             /* lại như cũ */
  color: #000000;
  line-height: 1.7;
  font-weight: 400;
  margin-top: auto;            /* đẩy xuống cuối card */
}

@media (max-width: 860px) {
  .steps { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .steps { grid-template-columns: 1fr; }
}
</style>
