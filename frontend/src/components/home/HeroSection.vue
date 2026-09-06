<template>
  <section class="hero">
    <!-- Full-width background video: autoplay, muted, loop, no controls -->
    <!-- :key ép <video> tải lại khi admin đổi video (src đổi không tự reload) -->
    <video
      class="hero-video"
      :key="videoSrc"
      :src="videoSrc"
      :poster="poster || undefined"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
    />

    <!-- Light dark overlay so any hero text stays legible -->
    <div class="hero-overlay" />
  </section>
</template>

<script setup>
// Video nền, không cần JS điều khiển (autoplay + loop + muted).
// Admin đổi video ở trang admin → Nội dung web; file mặc định nằm ở public/videos/.
import { computed } from 'vue'
import { useSiteSettings } from '@/composables/useSiteSettings'

const { settings } = useSiteSettings()

const videoSrc = computed(() => settings.value.hero_video?.url    || '/videos/hero.webm')
const poster   = computed(() => settings.value.hero_video?.poster || '/videos/hero-poster.jpg')
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  height: 100vh;
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
</style>
