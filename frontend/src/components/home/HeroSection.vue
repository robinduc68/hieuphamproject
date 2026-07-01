<template>
  <section class="hero">
    <!-- Full-width background video: autoplay, muted, loop, no controls -->
    <video
      class="hero-video"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
      :poster="poster"
    >
      <source :src="videoSrc" type="video/webm" />
    </video>

    <!-- Light dark overlay so any hero text stays legible -->
    <div class="hero-overlay" />
  </section>
</template>

<script setup>
// ponytail: pure background video, no JS controls needed (autoplay+loop+muted).
// Drop hero.webm in public/videos/ (poster optional).
const videoSrc = '/videos/hero.webm'
const poster   = '/videos/hero-poster.jpg'
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  height: 870px;
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
