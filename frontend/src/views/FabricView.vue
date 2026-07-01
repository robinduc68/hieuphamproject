<template>
  <div class="fabric-page">
    <div class="fabric-layout">

      <!-- ── Sidebar ─────────────────────────────────────── -->
      <aside class="fabric-sidebar">

        <!-- HỌA TIẾT -->
        <div class="filter-section">
          <h3 class="filter-title">HỌA TIẾT</h3>
          <input
            v-model="patternSearch"
            class="filter-search"
            type="text"
            placeholder="Tùy chọn tìm kiếm..."
          />
          <div class="pattern-list">
            <label
              v-for="p in filteredPatterns"
              :key="p"
              class="pattern-item"
            >
              <input type="checkbox" v-model="selectedPatterns" :value="p" />
              <span>{{ p }}</span>
            </label>
          </div>
        </div>

        <!-- MÀU SẮC -->
        <div class="filter-section">
          <h3 class="filter-title">MÀU SẮC</h3>
          <div class="color-grid">
            <div
              v-for="c in colors"
              :key="c.name"
              class="color-item"
              :class="{ selected: selectedColors.includes(c.name) }"
              @click="toggleColor(c.name)"
            >
              <div
                class="color-swatch"
                :style="{ background: c.hex, border: c.hex === '#FFFFFF' ? '1px solid #ddd' : 'none' }"
              />
              <span class="color-name">{{ c.name }}</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <button class="btn-filter" @click="applyFilter">TÌM THEO BỘ LỌC</button>
        <button class="btn-reset" @click="resetFilter">BỎ BỘ LỌC</button>

      </aside>

      <!-- ── Main grid ───────────────────────────────────── -->
      <main class="fabric-main">
        <p class="fabric-desc">Chọn mẫu vải để thiết kế bộ áo dài, pháp phục của riêng bạn.</p>

        <div class="fabric-grid">
          <RouterLink
            v-for="fabric in displayedFabrics"
            :key="fabric.id"
            :to="`/lua-to-tam/${fabric.id}`"
            class="fabric-card"
          >
            <div class="fabric-img" :style="{ background: fabricGradient(fabric.color1, fabric.color2) }">
              <div class="fabric-shimmer" />
            </div>
            <p class="fabric-name">{{ fabric.name }}</p>
          </RouterLink>
        </div>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { fabrics as allFabrics, patterns, colors, fabricGradient } from '@/data/fabrics'

const patternSearch   = ref('')
const selectedPatterns = ref([])
const selectedColors  = ref([])

const filteredPatterns = computed(() =>
  patterns.filter(p => p.toLowerCase().includes(patternSearch.value.toLowerCase()))
)

const displayedFabrics = computed(() => {
  let list = allFabrics
  if (selectedPatterns.value.length)
    list = list.filter(f => selectedPatterns.value.includes(f.pattern))
  if (selectedColors.value.length)
    list = list.filter(f => selectedColors.value.includes(f.colorTag))
  return list
})

function toggleColor(name) {
  const i = selectedColors.value.indexOf(name)
  if (i === -1) selectedColors.value.push(name)
  else selectedColors.value.splice(i, 1)
}

function applyFilter() { /* filter is already reactive */ }

function resetFilter() {
  selectedPatterns.value = []
  selectedColors.value   = []
  patternSearch.value    = ''
}

</script>

<style scoped>
.fabric-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: 100px 48px 64px;
}

.fabric-layout {
  display: flex;
  gap: 28px;
  max-width: 1300px;
  margin: 0 auto;
  align-items: flex-start;
}

/* ── Sidebar ─────────────────────────────────────────── */
.fabric-sidebar {
  width: 300px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.filter-section {
  margin-bottom: 24px;
}

.filter-title {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--brand-red);
  margin-bottom: 14px;
}

.filter-search {
  width: 100%;
  padding: 9px 16px;
  border: 1px solid #ddd;
  border-radius: 999px;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  outline: none;
  margin-bottom: 12px;
  transition: border-color var(--transition);
}
.filter-search:focus { border-color: var(--brand-red); }
.filter-search::placeholder { color: #bbb; }

.pattern-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.pattern-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 4px;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  transition: color var(--transition);
}
.pattern-item:hover { color: var(--brand-red); }
.pattern-item input[type="checkbox"] {
  accent-color: var(--brand-red);
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

/* Color grid */
.color-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px 8px;
}
.color-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}
.color-swatch {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  transition: transform var(--transition), box-shadow var(--transition);
}
.color-item:hover .color-swatch,
.color-item.selected .color-swatch {
  transform: scale(1.1);
  box-shadow: 0 0 0 2px var(--brand-red);
}
.color-name {
  font-family: var(--font-body);
  font-size: 11px;
  color: var(--text-dark);
  text-align: center;
}

/* Buttons */
.btn-filter {
  width: 100%;
  padding: 13px;
  background: var(--brand-red);
  border: none;
  border-radius: 999px;
  color: #fff;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background var(--transition);
}
.btn-filter:hover { background: var(--brand-dark); }

.btn-reset {
  width: 100%;
  padding: 12px;
  background: #fff;
  border: 1.5px solid var(--brand-red);
  border-radius: 999px;
  color: var(--brand-red);
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}
.btn-reset:hover { background: var(--brand-red); color: #fff; }

/* ── Main ────────────────────────────────────────────── */
.fabric-main {
  flex: 1;
  min-width: 0;
}

.fabric-desc {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-dark);
  margin-bottom: 24px;
}

.fabric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.fabric-card {
  cursor: pointer;
  display: block;
  color: inherit;
  text-decoration: none;
}

.fabric-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  margin-bottom: 10px;
  transition: transform var(--transition), box-shadow var(--transition);
}
.fabric-card:hover .fabric-img {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,.15);
}

.fabric-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0)    0%,
    rgba(255,255,255,.18) 45%,
    rgba(255,255,255,.32) 50%,
    rgba(255,255,255,.18) 55%,
    rgba(255,255,255,0)   100%
  );
  pointer-events: none;
}

.fabric-name {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: var(--text-dark);
  text-align: center;
  text-transform: uppercase;
}
</style>
