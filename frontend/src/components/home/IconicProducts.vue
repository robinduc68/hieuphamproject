<template>
  <section class="products-section" id="products">
    <div class="products-head">
      <h2 class="products-heading">ĐƯỢC TIN CHỌN NHIỀU NHẤT</h2>
    </div>

    <div class="carousel-wrap">

      <!-- Arrow left: cao bằng card, nền = màu nền, không shadow/border -->
      <button class="arrow arrow-left" @click="prev" aria-label="Trước">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>

      <!-- Viewport -->
      <div class="viewport" ref="viewportEl">
        <div
          class="track"
          :class="{ 'no-anim': !animate }"
          :style="{ transform: `translateX(-${currentIndex * (itemWidth + GAP)}px)` }"
        >
          <div
            v-for="(product, i) in loopProducts"
            :key="i"
            class="product-card"
            :style="{ width: itemWidth + 'px' }"
          >
            <RouterLink :to="`/san-pham/${product.slug}`" class="card-link">
              <div class="card-img">
                <img :src="product.image" :alt="product.name" />
              </div>
              <div class="card-info">
                <p class="card-name">{{ product.name }}</p>
                <p class="card-price">{{ product.price }}</p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Arrow right -->
      <button class="arrow arrow-right" @click="next" aria-label="Sau">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 18l6-6-6-6" />
        </svg>
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useInfiniteCarousel } from '@/composables/useInfiniteCarousel'

const products = [
  { id: 1, name: 'TÊN SẢN PHẨM', slug: 'san-pham-1', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/e8e4dc/888?text=Sản+phẩm+1' },
  { id: 2, name: 'TÊN SẢN PHẨM', slug: 'san-pham-2', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/ddd8cf/888?text=Sản+phẩm+2' },
  { id: 3, name: 'TÊN SẢN PHẨM', slug: 'san-pham-3', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/e4dfd6/888?text=Sản+phẩm+3' },
  { id: 4, name: 'TÊN SẢN PHẨM', slug: 'san-pham-4', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/d8d3ca/888?text=Sản+phẩm+4' },
  { id: 5, name: 'TÊN SẢN PHẨM', slug: 'san-pham-5', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/e0dbd2/888?text=Sản+phẩm+5' },
  { id: 6, name: 'TÊN SẢN PHẨM', slug: 'san-pham-6', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/dbd6cd/888?text=Sản+phẩm+6' },
  { id: 7, name: 'TÊN SẢN PHẨM', slug: 'san-pham-7', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/e6e1d8/888?text=Sản+phẩm+7' },
  { id: 8, name: 'TÊN SẢN PHẨM', slug: 'san-pham-8', price: '0.000.000 - 0.000.000 Đ', image: 'https://placehold.co/400x520/d6d1c8/888?text=Sản+phẩm+8' },
]

// Render 2× để carousel vô tận trượt mượt (real + clone)
const loopProducts = [...products, ...products]

const GAP        = 20
const viewportEl = ref(null)
const itemWidth  = ref(300)

const { currentIndex, animate, next, prev, reset } = useInfiniteCarousel(
  () => products.length,
  () => itemWidth.value + GAP
)

/* Số ảnh hiện cùng lúc (desktop = 4, không bị lấn nửa ảnh) */
function computeVisible() {
  const w = window.innerWidth
  return w > 1100 ? 4 : (w > 700 ? 3 : 2)
}

/* Tính độ rộng 1 ảnh theo CHIỀU RỘNG viewport để vừa đúng N ảnh nguyên */
function update() {
  if (!viewportEl.value) return
  const visible = computeVisible()
  itemWidth.value = Math.floor(
    (viewportEl.value.clientWidth - GAP * (visible - 1)) / visible
  )
}

function onResize() {
  update()
  reset()
}

/* ── Auto-play 15s ── */
let timer = null
function startAuto() {
  clearInterval(timer)
  timer = setInterval(next, 15000)
}

onMounted(() => {
  nextTick(update)
  requestAnimationFrame(update)
  window.addEventListener('resize', onResize)
  startAuto()
})
onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  clearInterval(timer)
})
</script>

<style scoped>
.products-section {
  background: var(--bg-gray);
  padding: 0;              /* bỏ padding – slideshow full bleed */
  padding-bottom: 30px;     /* khoảng trống dưới trước footer */
  display: flex;
  flex-direction: column;
}

.products-head {
  padding: 28px 2.5% 18px;  /* giữ padding ở title */
}

.products-heading {
  font-family: 'Philosopher', sans-serif;
  font-size: 27.9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: var(--brand-red);
}

/* Carousel: [arrow] [viewport] [arrow] – nút cao bằng card, tách rời khỏi ảnh */
.carousel-wrap {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 0;            /* nút chỉ 2.5%, hết chỗ còn lại cho ảnh */
}

.viewport {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.track {
  display: flex;
  gap: 20px;
  transition: transform 0.55s cubic-bezier(.25,.46,.45,.94);
  will-change: transform;
}
.track.no-anim { transition: none; }

/* Product card */
.product-card { flex-shrink: 0; }

.card-link {
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  text-decoration: none;
}

.card-img {
  width: 100%;
  aspect-ratio: 3 / 4;
  overflow: hidden;
  border-radius: 6px;
  background: #e0dbd3;
}
.card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .5s ease;
}
.card-link:hover .card-img img { transform: scale(1.04); }

.card-name  { font-size: 15px; font-weight: 600; color: var(--text-dark); }
.card-price { font-size: 13px; color: var(--brand-red); font-weight: 500; }

/* Arrows – cao bằng card, nền = màu nền trang, KHÔNG shadow/border/radius */
.arrow {
  flex-shrink: 0;
  width: 2.5%;        /* chỉ 2.5% – phần còn lại cho ảnh */
  border-radius: 0;
  background: var(--bg-gray);
  border: none;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--brand-red);
  transition: color var(--transition), transform var(--transition);
}
.arrow:hover {
  color: var(--brand-dark);
}
.arrow:hover svg { transform: scale(1.15); }
.arrow svg { width: 28px; height: 28px; transition: transform var(--transition); }

@media (max-width: 700px) {
  .arrow { width: 8%; }
  .arrow svg { width: 24px; height: 24px; }
}
</style>
