<template>
  <!-- SVG filter: xóa nền trắng/gần trắng của PNG logo -->
  <svg style="display:none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="mh-remove-white" color-interpolation-filters="sRGB">
        <feColorMatrix type="matrix"
          values="1 0 0 0 0
                  0 1 0 0 0
                  0 0 1 0 0
                 -1 -1 -1 3 0"/>
      </filter>
    </defs>
  </svg>

  <section class="about-section">
    <div class="about-card">

      <!-- Left: 2 staggered scrolling columns -->
      <div class="photo-ticker">
        <div class="col col-left">
          <div class="photo-track">
            <div v-for="photo in leftPhotos" :key="photo.id" class="photo-item">
              <img :src="photo.src" :alt="photo.alt" />
            </div>
          </div>
        </div>
        <div class="col col-right">
          <div class="photo-track">
            <div v-for="photo in rightPhotos" :key="photo.id" class="photo-item">
              <img :src="photo.src" :alt="photo.alt" />
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Brand panel -->
      <div class="about-panel">
        <div class="panel-logo" role="img" aria-label="Hà Hoạt Silk"></div>
        <p class="tagline"><em>Thương hiệu Di sản</em></p>
        <p class="desc">
          Lụa tơ tằm Nha Xá,<br/>
          được bảo chứng bởi<br/>
          <strong>Nghệ nhân Phạm Văn Hoạt.</strong>
        </p>
      </div>

    </div>
  </section>
</template>

<script setup>
const photos = [
  { src: '/general-1.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-2.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-3.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-4.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-5.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-6.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-1.jpg', alt: 'Hà Hoạt Silk' },
  { src: '/general-4.jpg', alt: 'Hà Hoạt Silk' },
]

// Split into left (even indices) and right (odd indices), each duplicated for seamless loop
const leftPhotos  = [...photos.filter((_, i) => i % 2 === 0), ...photos.filter((_, i) => i % 2 === 0)].map((p, i) => ({ ...p, id: i }))
const rightPhotos = [...photos.filter((_, i) => i % 2 === 1), ...photos.filter((_, i) => i % 2 === 1)].map((p, i) => ({ ...p, id: i }))
</script>

<style scoped>
.about-section {
  background: var(--bg-gray);
  padding: 56px 48px;
}

.about-card {
  max-width: 1272px;
  margin: 0 auto;
  background: #681927;
  border-radius: 16px;
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 14px;
  padding: 14px;
  overflow: hidden;
  box-shadow: 0 1px 16px rgba(0,0,0,.07);
  border: 1px solid rgba(0,0,0,.05);
  height: 720px;
}

/* ── Photo ticker ── */
.photo-ticker {
  overflow: hidden;
  background: #681927;
  border-radius: 10px;
  padding: 10px;
  display: flex;
  gap: 8px;
}

.col {
  flex: 1;
  overflow: hidden;
}

.photo-track {
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: scroll-up 26s linear infinite;
}

/* Right column starts offset by ~half a photo to stagger */
.col-right .photo-track {
  margin-top: -114px;
}

.photo-item {
  border-radius: 8px;
  overflow: hidden;
  line-height: 0;
  flex-shrink: 0;
  aspect-ratio: 4 / 3;
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

@keyframes scroll-up {
  from { transform: translateY(0); }
  to   { transform: translateY(-50%); }
}

/* ── Brand panel ── */
.about-panel {
  background: #F5F5F5;
  border-radius: 10px;
  padding: 40px 48px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 18px;
}

.panel-logo {
  width: 210px;
  height: 210px;
  background-image: url('/HHSLG.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.tagline {
  font-family: var(--font-script);
  font-size: 52px;
  color: var(--brand-red);
  line-height: 1.1;
}

.desc {
  font-size: 20px;
  line-height: 2;
  color: var(--text-dark);
  font-weight: 600;
}
.desc strong {
  font-family: 'Philosopher', sans-serif;
  font-style: italic;
  font-weight: 700;
  color: #681927;
}
</style>
