<template>
  <section class="hero">

    <!-- Video -->
    <div class="video-wrap">
      <video ref="videoEl" class="hero-video" muted loop playsinline />
      <div class="video-placeholder" />
    </div>

    <!-- Play button -->
    <button class="play-btn" @click="togglePlay" :aria-label="playing ? 'Tạm dừng' : 'Phát video'">
      <svg v-if="!playing" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>
      <svg v-else viewBox="0 0 24 24" fill="white"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
    </button>

    <!-- Progress bar -->
    <div class="progress-bar">
      <div class="progress-track" :style="{ width: progress + '%' }" />
    </div>

  </section>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const videoEl = ref(null)
const playing = ref(false)
const progress = ref(0)
let raf = null

function togglePlay() {
  if (!videoEl.value) return
  if (playing.value) {
    videoEl.value.pause(); playing.value = false; cancelAnimationFrame(raf)
  } else {
    videoEl.value.play(); playing.value = true; tick()
  }
}
function tick() {
  const v = videoEl.value
  if (v && v.duration) progress.value = (v.currentTime / v.duration) * 100
  raf = requestAnimationFrame(tick)
}

onUnmounted(() => cancelAnimationFrame(raf))
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  height: 72vh;
  min-height: 320px;
  overflow: hidden;
  background: #111;
}

/* ── Video ── */
.video-wrap { position: absolute; inset: 0; }
.hero-video  { width: 100%; height: 100%; object-fit: cover; }
.video-placeholder {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, #1a100e 0%, #2b1a15 40%, #1a1510 100%);
}

/* ── Play button ── */
.play-btn {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255,255,255,.12);
  border: 1.5px solid rgba(255,255,255,.55);
  border-radius: 50%; width: 72px; height: 72px;
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(6px);
  transition: background var(--transition), transform var(--transition);
  cursor: pointer; z-index: 10;
}
.play-btn:hover {
  background: rgba(255,255,255,.22);
  transform: translate(-50%, -50%) scale(1.06);
}
.play-btn svg { width: 28px; height: 28px; }

/* ── Progress ── */
.progress-bar {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 3px; background: rgba(255,255,255,.18); z-index: 10;
}
.progress-track {
  height: 100%; background: rgba(255,255,255,.8);
  transition: width .15s linear;
}
</style>
