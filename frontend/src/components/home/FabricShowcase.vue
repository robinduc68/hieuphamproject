<template>
  <section class="fabric-showcase">
    <div class="fs-row">
      <RouterLink
        v-for="f in fabrics"
        :key="f.name"
        to="/lua-to-tam"
        class="fs-card"
      >
        <div class="fs-swatch">
          <img :src="f.img" :alt="f.name" class="fs-img" />
          <span class="fs-shimmer" />
        </div>
        <p class="fs-name">{{ f.name }}</p>
      </RouterLink>
    </div>

    <RouterLink to="/lua-to-tam" class="fs-cta">
      Khám phá kho lụa
      <span class="fs-cta-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
          <path d="M7 17L17 7M17 7H8M17 7v9" />
        </svg>
      </span>
    </RouterLink>
  </section>
</template>

<script setup>
const fabrics = [
  { name: 'Thọ Dơi',       img: '/tho-doi.png' },
  { name: 'Đuôi Công',     img: '/duoi-cong.jpg' },
  { name: 'Cúc',           img: '/cuc.jpg' },
  { name: 'Thủy Tiên',     img: '/thuy-tien.jpg' },
  { name: 'Sen - Hồ Điệp', img: '/sen-ho-diep.png' },
]
</script>

<style scoped>
.fabric-showcase {
  background: var(--bg-gray);
  padding: 0 48px 80px;
}

.fs-row {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.fs-card { display: block; color: inherit; }

.fs-swatch {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition);
}
.fs-card:hover .fs-swatch {
  transform: translateY(-4px);
  box-shadow: 0 10px 26px rgba(0, 0, 0, .18);
}
.fs-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.fs-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg,
    rgba(255,255,255,0) 40%,
    rgba(255,255,255,.28) 50%,
    rgba(255,255,255,0) 60%);
}

.fs-name {
  margin-top: 12px;
  text-align: center;
  font-family: var(--font-display);
  font-size: 19px;
  font-weight: 600;
  color: var(--charcoal);
}

.fs-cta {
  margin: 40px auto 0;
  width: fit-content;
  display: flex;
  align-items: center;
  gap: 14px;
  background: #FFFFFF;
  color: var(--brand-red);
  border: 1px solid var(--brand-red);
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
  padding: 14px 14px 14px 28px;
  border-radius: 999px;
  transition: background var(--transition);
}
.fs-cta:hover { background: var(--cream); }
.fs-cta-icon {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--brand-red);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
}
.fs-cta-icon svg { width: 18px; height: 18px; }

@media (max-width: 860px) {
  .fs-row { grid-template-columns: repeat(2, 1fr); }
}
</style>
