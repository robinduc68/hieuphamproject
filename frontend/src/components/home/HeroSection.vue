<template>
  <section class="hero">
    <!-- Full-width background video: autoplay, muted, loop, no controls -->
    <!-- :key ép <video> tải lại khi admin đổi video (src đổi không tự reload) -->
    <!-- MP4 (H.264) trước: iPhone không phát được WebM/VP8 ⇒ đứng hình ở poster.
         Không có bản .mp4 cùng tên thì trình duyệt tự bỏ qua, dùng nguồn gốc. -->
    <video
      ref="videoEl"
      class="hero-video"
      :key="videoSrc"
      :poster="poster || undefined"
      autoplay
      muted
      loop
      playsinline
      webkit-playsinline
      preload="auto"
    >
      <source v-if="mp4Src" :src="mp4Src" type="video/mp4" />
      <source :src="videoSrc" />
    </video>

    <!-- Light dark overlay so any hero text stays legible -->
    <div class="hero-overlay" />
  </section>
</template>

<script setup>
// Video nền (autoplay + loop + muted).
// Admin đổi video ở trang admin → Nội dung web; file mặc định nằm ở public/videos/.
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useSiteSettings } from '@/composables/useSiteSettings'

const { settings } = useSiteSettings()

const videoSrc = computed(() => settings.value.hero_video?.url    || '/videos/hero.webm')
const poster   = computed(() => settings.value.hero_video?.poster || '/videos/hero-poster.jpg')
// Video .webm → thử bản .mp4 cùng tên trước (public/videos/hero.mp4)
const mp4Src   = computed(() => /\.webm$/i.test(videoSrc.value) ? videoSrc.value.replace(/\.webm$/i, '.mp4') : null)

/* Mobile chỉ cho autoplay khi video THẬT SỰ muted. Vue gán `muted` như
   property, không ghi ra attribute ⇒ iOS Safari coi là có tiếng và chặn.
   Ép lại muted + gọi play(). Máy vẫn chặn (iPhone bật Nguồn điện thấp,
   Data Saver…) thì phát ở lần chạm/cuộn đầu tiên. */
const videoEl = ref(null)
const GESTURES = ['touchstart', 'pointerdown', 'scroll', 'keydown']

function tryPlay() {
  const v = videoEl.value
  if (!v || !v.paused) return
  v.muted = true
  v.defaultMuted = true
  v.setAttribute('muted', '')
  v.play()?.catch(() => {})
}
function onVisible() { if (document.visibilityState === 'visible') tryPlay() }

watch(videoSrc, () => nextTick(tryPlay))   // :key đổi → thẻ <video> mới

onMounted(() => {
  tryPlay()
  GESTURES.forEach(e => window.addEventListener(e, tryPlay, { passive: true }))
  document.addEventListener('visibilitychange', onVisible)
})
onUnmounted(() => {
  GESTURES.forEach(e => window.removeEventListener(e, tryPlay))
  document.removeEventListener('visibilitychange', onVisible)
})
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  height: 100vh;
  /* svh = chiều cao thật khi thanh địa chỉ trình duyệt mobile đang hiện */
  height: 100svh;
  min-height: 320px;
  overflow: hidden;
  background: linear-gradient(135deg, #1a100e 0%, #2b1a15 40%, #1a1510 100%);
}

.hero-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.25);
  pointer-events: none;
}

@media (max-width: 768px) {
  .hero { height: 68svh; min-height: 420px; }
}

/* Mobile: khung 414 × 477 theo design */
@media (max-width: 767px) {
  .hero { height: 115.2vw; min-height: 320px; }
}
</style>
