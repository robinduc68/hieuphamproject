<template>
  <section class="about-section">
    <div class="about-card">

      <!-- Left: Photo grid -->
      <div class="photo-grid">
        <div class="photo p1">
          <img src="https://placehold.co/420x220/d4c4b0/777?text=Ảnh+1" alt="Giải thưởng" />
        </div>
        <div class="photo p2">
          <img src="https://placehold.co/240x140/c8b89a/777?text=Ảnh+2" alt="Lụa cuộn" />
        </div>
        <div class="photo p3">
          <img src="https://placehold.co/240x200/b8a888/777?text=Bằng+khen" alt="Bằng khen" />
        </div>
        <div class="photo p4">
          <img src="https://placehold.co/420x280/a89870/777?text=Lụa+màu" alt="Lụa màu sắc" />
        </div>
        <div class="photo p5">
          <img src="https://placehold.co/240x160/c0a870/777?text=Áo+dài" alt="Áo dài" />
        </div>
      </div>

      <!-- Right: Brand panel -->
      <div class="about-panel">
        <!-- Logo mark -->
        <div class="brand-mark">
          <svg viewBox="0 0 60 72" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Left stroke of H -->
            <rect x="4"  y="2"  width="7" height="38" rx="1" fill="#8B1A2E"/>
            <!-- Right stroke of H -->
            <rect x="49" y="2"  width="7" height="38" rx="1" fill="#8B1A2E"/>
            <!-- Curved crossbar ribbon -->
            <path d="M11 16 C24 26 36 22 49 16" stroke="#8B1A2E" stroke-width="3.5"
              fill="none" stroke-linecap="round"/>
            <!-- Silk spool at bottom right -->
            <ellipse cx="46" cy="54" rx="10" ry="4.5" stroke="#8B1A2E" stroke-width="1.4" fill="none"/>
            <line x1="36" y1="54" x2="36" y2="66" stroke="#8B1A2E" stroke-width="1.4"/>
            <line x1="56" y1="54" x2="56" y2="66" stroke="#8B1A2E" stroke-width="1.4"/>
            <ellipse cx="46" cy="66" rx="10" ry="4.5" stroke="#8B1A2E" stroke-width="1.4" fill="none"/>
            <!-- Thread from spool to left stroke -->
            <path d="M36 60 C26 55 14 45 11 30" stroke="#8B1A2E" stroke-width="0.8"
              fill="none" stroke-dasharray="2 2" opacity="0.5"/>
          </svg>
        </div>

        <!-- Brand name -->
        <div class="brand-name">
          <span class="name-script">Hà Hoạt</span>
          <span class="name-sub">Sil</span>
        </div>

        <!-- Tagline -->
        <p class="tagline"><em>Thương hiệu Di sản</em></p>

        <!-- Description -->
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
</script>

<style scoped>
.about-section {
  background: var(--bg-gray);
  padding: 56px 48px;
}

.about-card {
  max-width: 1060px;
  margin: 0 auto;
  background: #f7f5f2;
  border-radius: 16px;
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  overflow: hidden;
  box-shadow: 0 1px 16px rgba(0,0,0,.07);
  border: 1px solid rgba(0,0,0,.05);
}

/* ── Photo grid ── */
.photo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  padding: 12px;
  background: #ece8e2;
}

.photo { overflow: hidden; border-radius: 8px; line-height: 0; }
.photo img { width: 100%; height: 100%; object-fit: cover; display: block; }

/* Grid positions */
.p1 { grid-column: 1; grid-row: 1; }
.p2 { grid-column: 2; grid-row: 1; }
.p3 { grid-column: 2; grid-row: 2; }
.p4 { grid-column: 1; grid-row: 2 / 4; }
.p5 { grid-column: 2; grid-row: 3; }

/* ── Brand panel ── */
.about-panel {
  background: #faf9f7;
  padding: 40px 40px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  gap: 14px;
}

/* Logo mark SVG */
.brand-mark svg {
  width: 72px;
  height: 86px;
}

/* Brand name */
.brand-name {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1;
  margin-top: -4px;
}
.name-script {
  font-family: var(--font-script);
  font-size: 58px;
  color: var(--brand-red);
  line-height: 1.0;
}
.name-sub {
  font-family: var(--font-display);
  font-size: 16px;
  font-style: italic;
  font-weight: 600;
  color: var(--brand-red);
  letter-spacing: 4px;
  align-self: flex-end;
  margin-top: -6px;
}

/* Tagline */
.tagline {
  font-family: var(--font-script);
  font-size: 48px;
  color: var(--brand-red);
  font-weight: 400;
  line-height: 1.1;
  margin-top: 4px;
}

/* Description */
.desc {
  font-size: 17px;
  line-height: 2;
  color: var(--text-dark);
  font-weight: 500;
}
.desc strong {
  font-style: italic;
  font-weight: 700;
  color: var(--text-dark);
}
</style>
