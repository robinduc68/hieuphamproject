<template>
  <section class="fabric-showcase">
    <div class="fs-carousel">

      <!-- Arrow left -->
      <button class="fs-arrow fs-arrow-left" @click="prev" aria-label="Mẫu trước">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>

      <!-- Viewport -->
      <div class="fs-viewport" ref="viewportEl">
        <div
          class="fs-track"
          :class="{ 'no-anim': !animate }"
          :style="{ transform: `translateX(-${currentIndex * (itemWidth + GAP)}px)` }"
        >
          <RouterLink
            v-for="(f, i) in loopFabrics"
            :key="i"
            to="/lua-to-tam"
            class="fs-card"
            :style="{ width: itemWidth + 'px' }"
          >
            <div class="fs-swatch">
              <img :src="f.img" :alt="f.name" class="fs-img" />
              <span class="fs-shimmer" />
            </div>
            <p class="fs-name">{{ f.name }}</p>
          </RouterLink>
        </div>
      </div>

      <!-- Arrow right -->
      <button class="fs-arrow fs-arrow-right" @click="next" aria-label="Mẫu sau">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
          <path d="M9 18l6-6-6-6" />
        </svg>
      </button>
    </div>

    <RouterLink to="/lua-to-tam" class="fs-cta">
      Khám phá kho lụa
      <span class="fs-cta-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
          <path d="M7 17L17 7M17 7H8M17 7v9" />
        </svg>
      </span>
    </RouterLink>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useInfiniteCarousel } from '@/composables/useInfiniteCarousel'

const fabrics = [
  { name: 'Thọ Dơi',       img: '/tho-doi.png' },
  { name: 'Đuôi Công',     img: '/duoi-cong.jpg' },
  { name: 'Cúc',           img: '/cuc.jpg' },
  { name: 'Thủy Tiên',     img: '/thuy-tien.jpg' },
  { name: 'Sen - Hồ Điệp', img: '/sen-ho-diep.png' },
]

// Render 2× để carousel vô tận trượt mượt (real + clone)
const loopFabrics = [...fabrics, ...fabrics]

const GAP        = 20
const viewportEl = ref(null)
const itemWidth  = ref(240)

const { currentIndex, animate, next, prev, reset } = useInfiniteCarousel(
  () => fabrics.length,
  () => itemWidth.value + GAP
)

function computeVisible() {
  const w = window.innerWidth
  return w > 980 ? 4 : (w > 620 ? 3 : 2)
}

function updateItemWidth() {
  if (!viewportEl.value) return
  const visible = computeVisible()
  itemWidth.value = Math.floor(
    (viewportEl.value.offsetWidth - GAP * (visible - 1)) / visible
  )
}

function onResize() {
  updateItemWidth()
  reset()
}

onMounted(() => {
  updateItemWidth()
  window.addEventListener('resize', onResize)
  startAuto()
})
onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  clearInterval(timer)
})

/* ── Auto-play ~4.5s (tự chạy giống slideshow dưới) ── */
let timer = null
function startAuto() {
  clearInterval(timer)
  timer = setInterval(next, 4500)
}
</script>

<style scoped>
.fabric-showcase {
  background: var(--bg-gray);
  padding: 0 20px 48px;
}

/* Carousel */
.fs-carousel {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
}

.fs-viewport {
  flex: 1;
  overflow: hidden;
}

.fs-track {
  display: flex;
  gap: 20px;
  transition: transform 0.55s cubic-bezier(.25,.46,.45,.94);
  will-change: transform;
}
.fs-track.no-anim { transition: none; }

.fs-card { display: block; color: inherit; flex-shrink: 0; }

.fs-swatch {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition);
}
.fs-card:hover .fs-swatch {
  transform: translateY(-4px);
  box-shadow: 0 10px 26px rgba(0, 0, 0, .18);
}
.fs-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.fs-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg,
    rgba(255,255,255,0) 40%,
    rgba(255,255,255,.28) 50%,
    rgba(255,255,255,0) 60%);
}

.fs-name {
  margin-top: 12px;
  text-align: center;
  font-family: var(--font-display);
  font-size: 19px;
  font-weight: 600;
  color: var(--charcoal);
}

/* Arrows */
.fs-arrow {
  flex-shrink: 0;
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--brand-red);
  box-shadow: 0 2px 12px rgba(0,0,0,.1);
  transition: all var(--transition);
}
.fs-arrow:hover {
  background: var(--brand-red);
  border-color: var(--brand-red);
  color: #FFFFFF;
}
.fs-arrow svg { width: 20px; height: 20px; }

/* CTA – nền = màu chữ cũ, chữ = màu nền cũ, to & đậm hơn */
.fs-cta {
  margin: 40px auto 0;
  width: fit-content;
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--brand-red);
  color: #FFFFFF;
  border: 1px solid var(--brand-red);
  font-family: var(--font-body);
  font-size: 18px;
  font-weight: 700;
  padding: 16px 18px 16px 34px;
  border-radius: 999px;
  transition: background var(--transition), transform var(--transition);
}
.fs-cta:hover {
  background: var(--brand-dark);
  transform: translateY(-2px);
}
.fs-cta-icon {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #FFFFFF;
  color: var(--brand-red);
  display: flex;
  align-items: center;
  justify-content: center;
}
.fs-cta-icon svg { width: 18px; height: 18px; }
</style>
