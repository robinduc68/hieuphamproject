<template>
  <article class="product-card" @mouseenter="hovered = true" @mouseleave="hovered = false">
    <RouterLink :to="`/san-pham/${product.slug}`" class="product-link">
      <!-- Image area -->
      <div class="product-img">
        <!-- Color swatch as placeholder (real impl would use <img>) -->
        <div
          class="product-swatch"
          :style="{
            background: `linear-gradient(160deg, ${product.color}22 0%, ${product.color}44 100%)`,
          }"
        >
          <div class="swatch-ornament" aria-hidden="true">
            <svg viewBox="0 0 100 130" fill="none" :style="{ opacity: hovered ? .18 : .1, transition: 'opacity .4s' }">
              <rect x="2" y="2" width="96" height="126" stroke="currentColor" stroke-width=".8"/>
              <line x1="2" y1="40" x2="98" y2="40" stroke="currentColor" stroke-width=".4"/>
              <ellipse cx="50" cy="80" rx="22" ry="30" stroke="currentColor" stroke-width=".6"/>
              <circle cx="50" cy="80" r="5" stroke="currentColor" stroke-width=".5"/>
            </svg>
          </div>
          <span
            class="swatch-label"
            :style="{ color: product.color }"
          >{{ product.name.split('–')[0].trim() }}</span>
        </div>

        <!-- Badge -->
        <span v-if="product.isNew" class="product-badge">Mới</span>

        <!-- Quick add overlay -->
        <div class="quick-add" :class="{ visible: hovered }">
          <button class="quick-add-btn" @click.prevent="emit('quickAdd', product)">
            Thêm nhanh
          </button>
        </div>
      </div>

      <!-- Info -->
      <div class="product-info">
        <h3 class="product-name">{{ product.name }}</h3>
        <p class="product-price">{{ formatPrice(product.price) }}</p>
      </div>
    </RouterLink>

    <!-- Sizes -->
    <div class="product-sizes" aria-label="Chọn size">
      <button
        v-for="size in product.sizes"
        :key="size"
        class="size-chip"
        :class="{ active: selectedSize === size }"
        @click="selectedSize = size"
        :aria-label="`Size ${size}`"
      >{{ size }}</button>
    </div>
  </article>
</template>

<script setup>
import { ref } from 'vue'
import { formatPrice } from '@/utils/price'

const props = defineProps({
  product: { type: Object, required: true },
})

const emit = defineEmits(['quickAdd'])

const hovered     = ref(false)
const selectedSize = ref(null)
</script>

<style scoped>
.product-card { cursor: pointer; }

.product-link { display: block; color: inherit; }

/* Image */
.product-img {
  aspect-ratio: 3 / 4;
  position: relative;
  overflow: hidden;
  margin-bottom: 16px;
  background: var(--cream-dark);
}

.product-swatch {
  width: 100%; height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: transform .55s cubic-bezier(.25,.46,.45,.94);
}
.product-card:hover .product-swatch { transform: scale(1.04); }

.swatch-ornament {
  position: absolute;
  inset: 0;
  display: flex; align-items: center; justify-content: center;
  color: var(--charcoal);
}
.swatch-ornament svg { width: 70%; height: 70%; }

.swatch-label {
  font-family: var(--font-display);
  font-size: 15px;
  font-style: italic;
  font-weight: 400;
  text-align: center;
  padding: 0 12px;
  position: relative;
  z-index: 1;
  line-height: 1.3;
}

/* Badge */
.product-badge {
  position: absolute;
  top: 12px; left: 12px;
  background: var(--charcoal);
  color: var(--cream);
  font-size: 8px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  padding: 5px 10px;
  z-index: 2;
}

/* Quick add */
.quick-add {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 16px;
  background: linear-gradient(to top, rgba(26,26,24,.85), transparent);
  transform: translateY(100%);
  transition: transform .3s ease;
  z-index: 3;
}
.quick-add.visible { transform: translateY(0); }

.quick-add-btn {
  width: 100%;
  background: var(--cream);
  color: var(--charcoal);
  border: none;
  font-family: var(--font-body);
  font-size: 9px;
  letter-spacing: 3px;
  text-transform: uppercase;
  padding: 11px;
  font-weight: 500;
  transition: background var(--transition), color var(--transition);
}
.quick-add-btn:hover { background: var(--gold); color: var(--charcoal); }

/* Info */
.product-name {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 6px;
  transition: color var(--transition);
}
.product-card:hover .product-name { color: var(--gold); }

.product-price {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 12px;
  letter-spacing: .5px;
}

/* Sizes */
.product-sizes {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.size-chip {
  font-size: 9px;
  letter-spacing: 1px;
  border: 1px solid var(--border);
  padding: 4px 8px;
  color: var(--text-muted);
  background: transparent;
  font-family: var(--font-body);
  transition: all var(--transition);
}
.size-chip:hover,
.size-chip.active {
  border-color: var(--charcoal);
  background: var(--charcoal);
  color: var(--cream);
}
</style>
