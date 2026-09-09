<template>
  <section class="featured" aria-label="Sản phẩm nổi bật">
    <div class="featured-header">
      <span class="section-label" style="color: var(--gold-light)">Nổi Bật</span>
      <h2 class="section-title" style="color: var(--cream)">Được Yêu Thích Nhất</h2>
    </div>

    <div
      class="carousel-viewport"
      ref="viewport"
      @mousedown="startDrag"
      @mousemove="onDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @touchstart.passive="startDrag"
      @touchend="endDrag"
    >
      <div
        class="carousel-track"
        :style="{ transform: `translateX(${-currentIndex * slideWidth}px)`, transition: isDragging ? 'none' : 'transform .5s cubic-bezier(.25,.46,.45,.94)' }"
      >
        <RouterLink
          v-for="(item, i) in products"
          :key="item.id"
          :to="`/san-pham/${item.slug}`"
          class="carousel-slide"
          :style="{ '--accent': primaryColor(item) }"
          :aria-label="`${item.name} – ${item.sub_category}`"
        >
          <!-- Gradient image placeholder -->
          <div class="slide-img">
            <div class="slide-bg" :style="{ background: `linear-gradient(160deg, ${primaryColor(item)}18 0%, ${primaryColor(item)}35 100%)` }" />
            <div class="slide-overlay" />
            <div class="slide-ornament" aria-hidden="true">
              <svg viewBox="0 0 140 180" fill="none">
                <rect x="2" y="2" width="136" height="176" stroke="currentColor" stroke-width=".6" opacity=".15"/>
                <ellipse cx="70" cy="90" rx="35" ry="50" stroke="currentColor" stroke-width=".5" opacity=".12"/>
                <line x1="70" y1="20" x2="70" y2="160" stroke="currentColor" stroke-width=".3" opacity=".1"/>
              </svg>
            </div>
            <div class="slide-content">
              <span class="slide-number" aria-hidden="true">0{{ i + 1 }}</span>
              <div class="slide-info">
                <p class="slide-category">{{ item.sub_category }}</p>
                <h3 class="slide-name">{{ item.name }}</h3>
                <span class="slide-arrow">→</span>
              </div>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>

    <!-- Controls -->
    <div class="carousel-controls">
      <div class="carousel-dots" role="tablist" aria-label="Điều hướng carousel">
        <button
          v-for="(_, i) in products"
          :key="i"
          class="carousel-dot"
          :class="{ active: currentIndex === i }"
          role="tab"
          :aria-selected="currentIndex === i"
          :aria-label="`Slide ${i + 1}`"
          @click="goTo(i)"
        />
      </div>

      <div class="carousel-btns">
        <button class="carousel-btn" aria-label="Trước" @click="prev" :disabled="currentIndex === 0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <button class="carousel-btn" aria-label="Tiếp theo" @click="next" :disabled="currentIndex >= products.length - 1">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useFeaturedProducts } from '@/composables/useProducts'

const { products } = useFeaturedProducts(4)

function primaryColor(item) {
  return item.images?.[0]?.color_hex ?? '#b8972a'
}

const currentIndex = ref(0)
const slideWidth   = ref(0)
const viewport     = ref(null)
const isDragging   = ref(false)
let   dragStartX   = 0
let   autoTimer    = null

function goTo(i) {
  currentIndex.value = Math.max(0, Math.min(i, products.value.length - 1))
}
function prev() { goTo(currentIndex.value - 1) }
function next() { goTo(currentIndex.value + 1) }

/** Toạ độ X của cả chuột lẫn chạm */
function pointerX(e) {
  return e.changedTouches ? e.changedTouches[0].clientX : e.clientX
}

function startDrag(e) {
  isDragging.value = true
  dragStartX = pointerX(e)
}
function onDrag(e) {
  if (!isDragging.value) return
}
function endDrag(e) {
  if (!isDragging.value) return
  const delta = pointerX(e) - dragStartX
  if (Math.abs(delta) > 50) {
    delta < 0 ? next() : prev()
  }
  isDragging.value = false
}

function startAuto() {
  autoTimer = setInterval(() => {
    if (currentIndex.value >= products.value.length - 1) currentIndex.value = 0
    else next()
  }, 4500)
}

onMounted(() => {
  if (viewport.value) {
    slideWidth.value = viewport.value.offsetWidth
    const ro = new ResizeObserver(entries => {
      slideWidth.value = entries[0].contentRect.width
    })
    ro.observe(viewport.value)
    onUnmounted(() => ro.disconnect())
  }
  startAuto()
})
onUnmounted(() => clearInterval(autoTimer))
</script>

<style scoped>
.featured {
  background: var(--charcoal);
  padding: var(--section-y) 0 64px;
  overflow: hidden;
}

.featured-header {
  padding: 0 var(--page-x);
  margin-bottom: 48px;
}
.featured-header .section-title { margin-bottom: 0; }

/* Carousel */
.carousel-viewport {
  overflow: hidden;
  cursor: grab;
  user-select: none;
}
.carousel-viewport:active { cursor: grabbing; }

.carousel-track {
  display: flex;
}

.carousel-slide {
  flex: 0 0 100%;
  padding: 0 var(--page-x);
  display: block;
}

.slide-img {
  aspect-ratio: 21 / 9;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
}

.slide-bg {
  position: absolute;
  inset: 0;
  transition: transform .8s cubic-bezier(.25,.46,.45,.94);
}
.carousel-slide:hover .slide-bg { transform: scale(1.03); }

.slide-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(26,26,24,.9) 0%, rgba(26,26,24,.3) 50%, rgba(26,26,24,.6) 100%);
}

.slide-ornament {
  position: absolute;
  right: 80px;
  top: 50%;
  transform: translateY(-50%);
  width: 140px;
  height: 180px;
  color: var(--cream);
}

.slide-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: flex-end;
  gap: 32px;
  padding: 48px var(--page-x);
  width: 100%;
}

.slide-number {
  font-family: var(--font-display);
  font-size: 96px;
  font-weight: 300;
  color: rgba(245,240,232,.06);
  line-height: 1;
  flex-shrink: 0;
}

.slide-info { flex: 1; }

.slide-category {
  font-size: 10px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 10px;
}

.slide-name {
  font-family: var(--font-display);
  font-size: clamp(32px, 4vw, 56px);
  font-weight: 300;
  color: var(--cream);
  line-height: 1.1;
  margin-bottom: 20px;
  text-transform: uppercase;
}

.slide-arrow {
  font-size: 18px;
  color: var(--gold);
  display: inline-block;
  opacity: 0;
  transform: translateX(-12px);
  transition: opacity var(--transition), transform var(--transition);
}
.carousel-slide:hover .slide-arrow { opacity: 1; transform: translateX(0); }

/* Controls */
.carousel-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px var(--page-x) 0;
}

.carousel-dots {
  display: flex;
  gap: 8px;
}
.carousel-dot {
  width: 24px; height: 2px;
  background: rgba(245,240,232,.2);
  border: none;
  cursor: pointer;
  transition: background var(--transition), width var(--transition);
  padding: 0;
}
.carousel-dot.active {
  background: var(--gold);
  width: 40px;
}

.carousel-btns { display: flex; gap: 8px; }
.carousel-btn {
  width: 44px; height: 44px;
  border: 1px solid var(--border-dark);
  background: transparent;
  color: var(--cream);
  display: flex; align-items: center; justify-content: center;
  transition: border-color var(--transition), color var(--transition), background var(--transition);
}
.carousel-btn svg { width: 18px; height: 18px; }
.carousel-btn:hover:not(:disabled) {
  border-color: var(--gold);
  color: var(--gold);
}
.carousel-btn:disabled { opacity: .25; cursor: default; }

@media (max-width: 900px) {
  .slide-img      { aspect-ratio: 4 / 3; }
  .slide-number   { font-size: 60px; }
  .slide-name     { font-size: clamp(24px, 6vw, 34px); margin-bottom: 14px; }
  .slide-content  { gap: 18px; padding: 28px var(--page-x); }
  .slide-ornament { right: 20px; width: 92px; height: 120px; opacity: .5; }
  .featured-header { margin-bottom: 28px; }
}
@media (max-width: 560px) {
  .slide-img      { aspect-ratio: 3 / 4; }
  .slide-ornament { display: none; }
  .slide-number   { display: none; }
  .slide-overlay  { background: linear-gradient(to top, rgba(26,26,24,.92) 12%, rgba(26,26,24,.28) 70%); }
  .slide-arrow    { opacity: 1; transform: none; }   /* không có hover trên mobile */
}
</style>
