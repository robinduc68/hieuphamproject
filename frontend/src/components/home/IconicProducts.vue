<template>
  <section class="products-section">
    <div class="products-inner">
      <h2 class="products-heading">ĐƯỢC TIN CHỌN NHIỀU NHẤT</h2>

      <div class="carousel-wrap">

        <!-- Arrow left -->
        <button class="arrow arrow-left" @click="prev" :class="{ hidden: currentIndex === 0 }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M15 18l-6-6 6-6"/>
          </svg>
        </button>

        <!-- Viewport -->
        <div class="viewport" ref="viewportEl">
          <div class="track" :style="{ transform: `translateX(-${currentIndex * (itemWidth + GAP)}px)` }">
            <div
              v-for="product in products"
              :key="product.id"
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
        <button class="arrow arrow-right" @click="next" :class="{ hidden: currentIndex >= maxIndex }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 18l6-6-6-6"/>
          </svg>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

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

const VISIBLE    = 4
const GAP        = 20
const viewportEl = ref(null)
const itemWidth  = ref(300)
const currentIndex = ref(0)

const maxIndex = computed(() => products.length - VISIBLE)

function updateItemWidth() {
  if (!viewportEl.value) return
  // width chính xác: trừ tổng gap giữa 4 item
  itemWidth.value = Math.floor((viewportEl.value.offsetWidth - GAP * (VISIBLE - 1)) / VISIBLE)
}

function prev() {
  if (currentIndex.value > 0) currentIndex.value--
}

function next() {
  if (currentIndex.value < maxIndex.value) currentIndex.value++
  else currentIndex.value = 0 // loop về đầu
}

/* ── Auto-play 15s ── */
let timer = null

function startAuto() {
  clearInterval(timer)
  timer = setInterval(next, 15000)
}

onMounted(() => {
  updateItemWidth()
  window.addEventListener('resize', updateItemWidth)
  startAuto()
})
onUnmounted(() => {
  window.removeEventListener('resize', updateItemWidth)
  clearInterval(timer)
})
</script>

<style scoped>
.products-section {
  background: var(--bg-gray);
  padding: 72px 0 72px 48px;
}

.products-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding-right: 48px;
}

.products-heading {
  font-family: 'Philosopher', sans-serif;
  font-size: 27.9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: var(--brand-red);
  margin-bottom: 32px;
}

/* Carousel */
.carousel-wrap {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0;
}

.viewport {
  flex: 1;
  overflow: hidden;
  /* clip chính xác, không cho ảnh trước/sau lộ ra */
}

.track {
  display: flex;
  gap: 20px;
  transition: transform 0.55s cubic-bezier(.25,.46,.45,.94);
  will-change: transform;
}

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
  overflow: hidden;
  border-radius: 4px;
  background: #e0dbd3;
  aspect-ratio: 3 / 4;
}
.card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .5s ease;
}
.card-link:hover .card-img img { transform: scale(1.04); }

.card-name  { font-size: 13px; font-weight: 600; color: var(--text-dark); }
.card-price { font-size: 12px; color: var(--brand-red); font-weight: 500; }

/* Arrows */
.arrow {
  position: absolute;
  top: 40%;
  transform: translateY(-50%);
  z-index: 10;
  background: white;
  border: 1px solid var(--border);
  border-radius: 50%;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: 0 2px 12px rgba(0,0,0,.1);
}
.arrow:hover { background: var(--brand-red); border-color: var(--brand-red); color: white; }
.arrow svg { width: 18px; height: 18px; }
.arrow.hidden { opacity: 0; pointer-events: none; }

.arrow-left  { left: -22px; }
.arrow-right { right: -22px; }
</style>
