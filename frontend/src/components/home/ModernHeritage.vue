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
          Lụa tơ tằm Nha Xá,<br class="br-desktop"/>
          được bảo chứng bởi<br/>
          <strong>Nghệ nhân Phạm Văn Hoạt.</strong>
        </p>
      </div>

    </div>

    <!-- Mobile: dải ảnh tự chạy ngang (desktop dùng photo-ticker ở trên).
         Render 2 lần để marquee lặp liền mạch; bản sao ẩn với trình đọc màn hình. -->
    <div class="photo-strip">
      <div class="strip-track">
        <div
          v-for="(photo, i) in stripPhotos"
          :key="i"
          class="strip-item"
          :aria-hidden="i >= stripPhotos.length / 2 ? 'true' : null"
        >
          <img :src="photo.src" :alt="photo.alt" width="153" height="153" loading="lazy" decoding="async" />
        </div>
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

const stripPhotos = [...photos.slice(0, 6), ...photos.slice(0, 6)]

// Split into left (even indices) and right (odd indices), each duplicated for seamless loop
const leftPhotos  = [...photos.filter((_, i) => i % 2 === 0), ...photos.filter((_, i) => i % 2 === 0)].map((p, i) => ({ ...p, id: i }))
const rightPhotos = [...photos.filter((_, i) => i % 2 === 1), ...photos.filter((_, i) => i % 2 === 1)].map((p, i) => ({ ...p, id: i }))
</script>

<style scoped>
.about-section {
  background: var(--bg-gray);
  padding: 0;
}

.about-card {
  max-width: none;
  margin: 0;
  background: var(--brand-red);   /* viền/khung đỏ – khớp màu chữ trong panel */
  border-radius: 0;
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 14px;
  padding: 14px;
  overflow: hidden;
  box-shadow: none;
  border: none;
  height: 100vh;
  min-height: 560px;
}

/* ── Photo ticker ── */
.photo-ticker {
  overflow: hidden;
  background: var(--brand-red);
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
  padding: 40px var(--page-x);
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

@media (max-width: 860px) {
  .about-card { margin: 0; }
}

@media (max-width: 900px) {
  .about-card { grid-template-columns: 1fr; gap: 0; }
}

.photo-strip { display: none; }

/* ─── MOBILE (< 768px) ─── */
@media (max-width: 767px) {
  .about-section {
    background: var(--brand-red);
    padding: 25px 0 32px;
  }

  .about-card {
    display: block;
    height: auto;
    min-height: 0;
    padding: 0 18px;
  }
  .photo-ticker { display: none; }

  /* Card: logo trái (chiếm 2 hàng) – tagline + mô tả bên phải */
  .about-panel {
    display: grid;
    grid-template-columns: 68px 1fr;
    align-items: center;
    column-gap: 14px;
    row-gap: 4px;
    padding: 16px 14px 16px 16px;
    background: var(--bg-light);
  }
  .panel-logo {
    grid-row: 1 / 3;
    width: 68px;
    height: 76px;
  }
  .tagline { font-size: 30px; line-height: 1; align-self: end; }
  .desc {
    font-size: 14px;
    line-height: 1.5;
    font-weight: 400;
    align-self: start;
  }
  .desc strong { font-size: 15px; }
  .br-desktop { display: none; }

  /* Dải ảnh tự chạy ngang (marquee) – ảnh đầu/cuối luôn bị cắt ở mép */
  .photo-strip {
    display: block;
    margin-top: 26px;
    overflow: hidden;
  }
  .strip-track {
    display: flex;
    width: max-content;
    animation: strip-left 30s linear infinite;
  }
  /* Chạm giữ để dừng xem ảnh */
  .photo-strip:active .strip-track { animation-play-state: paused; }

  .strip-item {
    flex: 0 0 153px;
    margin-right: 7px;            /* margin thay gap → -50% khớp đúng 1 vòng */
    aspect-ratio: 1 / 1;
    border-radius: 8px;
    overflow: hidden;
  }
  .strip-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

@keyframes strip-left {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

@media (prefers-reduced-motion: reduce) {
  .strip-track { animation: none; }
  .photo-strip { overflow-x: auto; scrollbar-width: none; }
}
</style>
