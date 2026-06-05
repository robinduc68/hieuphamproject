<template>
  <section class="quote-section">
    <div class="quote-box">
      <p
        v-for="(line, i) in lines"
        :key="i"
        :ref="el => { if (el) lineEls[i] = el }"
        class="quote-line"
        :style="{ color: colors[i] }"
      ><em v-if="line.italic">{{ line.text }}</em><template v-else>{{ line.text }}</template></p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const lines = [
  { text: 'Hà Hoạt Silk hiểu rằng,',                  italic: false },
  { text: 'bộ đồ "đẹp" nhất không phải',              italic: false },
  { text: 'những gì chạy theo số đông, mà là',        italic: false },
  { text: 'lựa chọn độc bản phù hợp nhất,',           italic: true  },
  { text: 'mang câu chuyện của riêng bạn.',            italic: true  },
]

const lineEls = new Array(lines.length).fill(null)
const colors  = ref(lines.map(l => l.italic ? 'rgba(139,26,46,0.15)' : 'rgba(26,26,26,0.15)'))

const TRIGGER = 0.55   // đường reveal: 55% từ top màn hình
const FADE    = 70     // px vùng chuyển tiếp

function update() {
  const winH     = window.innerHeight
  const triggerY = winH * TRIGGER
  for (let i = 0; i < lines.length; i++) {
    const el = lineEls[i]
    if (!el) continue
    const midY = el.getBoundingClientRect().top + el.offsetHeight / 2
    let t
    if      (midY < triggerY - FADE) t = 1
    else if (midY > triggerY + FADE) t = 0
    else t = 1 - (midY - (triggerY - FADE)) / (FADE * 2)
    const a = 0.15 + Math.max(0, Math.min(1, t)) * 0.85
    colors.value[i] = lines[i].italic
      ? `rgba(139,26,46,${a})`
      : `rgba(26,26,26,${a})`
  }
}

let raf = null
function onScroll() {
  if (raf) return
  raf = requestAnimationFrame(() => { update(); raf = null })
}
onMounted(() => { window.addEventListener('scroll', onScroll, { passive: true }); update() })
onUnmounted(() => { window.removeEventListener('scroll', onScroll); if (raf) cancelAnimationFrame(raf) })
</script>

<style scoped>
.quote-section {
  background: #ECEAE7;
  padding: 110px 48px;
}

.quote-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  text-align: center;
}

.quote-line {
  font-family: var(--font-display);
  font-size: clamp(28px, 2.8vw, 42px);
  font-weight: 400;
  line-height: 1.75;
  letter-spacing: 0.3px;
  white-space: nowrap;
  transition: color 0.06s linear;
}

.quote-line em {
  font-style: italic;
  font-weight: 500;
}
</style>
