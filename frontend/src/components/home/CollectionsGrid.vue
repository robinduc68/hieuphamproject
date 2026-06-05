<template>
  <section class="features-section">
    <div class="features-inner">
      <!-- Left title -->
      <div class="features-title">
        <p class="title-script">Đặc quyền</p>
        <p class="title-regular">của lựa chọn</p>
        <p class="title-italic">Custom-Made</p>
      </div>

      <!-- Right: 4 cards -->
      <div class="features-cards">
        <div v-for="feat in features" :key="feat.title" class="feat-card">
          <div class="feat-icon" v-html="feat.icon" />
          <h3 class="feat-title">{{ feat.title }}</h3>
          <p class="feat-desc">{{ feat.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    title: 'Thiết kế riêng\nđộc nhất',
    desc: 'Không tồn tại sản phẩm thứ hai hoàn toàn giống "tác phẩm" bạn tạo nên.',
    icon: `<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M12 28 L20 10 L22 16 L30 14 L20 32 Z" stroke-linejoin="round"/>
      <circle cx="22" cy="16" r="2" fill="currentColor" stroke="none"/>
    </svg>`,
  },
  {
    title: 'Vừa vặn\ntừng đường nét',
    desc: 'Tùy chọn may theo bảng kích thước sản phẩm hoặc số đo cá nhân, miễn sao phù hợp với bạn.',
    icon: `<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M8 32 L20 8 L32 32 Z" stroke-linejoin="round"/>
      <line x1="8" y1="32" x2="32" y2="32"/>
      <line x1="14" y1="24" x2="26" y2="24"/>
    </svg>`,
  },
  {
    title: 'Trọn vẹn\ntrải nghiệm',
    desc: 'Trọn gói mọi trải nghiệm với lụa tơ tằm, từ chọn vải, chọn họa tiết, chọn cách may.',
    icon: `<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="8" y="14" width="24" height="18" rx="2"/>
      <path d="M14 14 V10 a6 6 0 0 1 12 0 v4"/>
      <path d="M16 24 L18 26 L24 20"/>
    </svg>`,
  },
  {
    title: 'Hỗ trợ\nlâu dài',
    desc: 'Đồng hành cùng bạn chăm sóc, bảo quản sản phẩm bền đẹp.',
    icon: `<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M10 20 a10 10 0 1 1 20 0" stroke-linecap="round"/>
      <path d="M8 20 Q8 26 12 26 L12 14 Q8 14 8 20"/>
      <path d="M32 20 Q32 26 28 26 L28 14 Q32 14 32 20"/>
      <path d="M20 30 Q24 30 26 28"/>
    </svg>`,
  },
]
</script>

<style scoped>
.features-section {
  background: var(--bg-gray);
  padding: 80px 48px;
}

.features-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 260px 1fr;
  align-items: center;
  gap: 56px;
}

/* Title block */
.features-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-script {
  font-family: var(--font-script);
  font-size: 48px;
  color: var(--text-dark);
  line-height: 1.05;
}

.title-regular {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--text-dark);
  font-weight: 400;
  margin-top: 2px;
}

.title-italic {
  font-family: var(--font-display);
  font-size: 22px;
  font-style: italic;
  color: var(--brand-red);
  font-weight: 500;
  margin-top: 2px;
}

/* Cards */
.features-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.feat-card {
  background: var(--bg-white);
  border-radius: var(--radius);
  padding: 28px 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: box-shadow var(--transition);
}
.feat-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,.08); }

.feat-icon {
  color: var(--text-dark);
  width: 36px;
  height: 36px;
}
.feat-icon :deep(svg) { width: 36px; height: 36px; }

.feat-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-dark);
  line-height: 1.45;
  white-space: pre-line;
}

.feat-desc {
  font-size: 12px;
  color: var(--text-medium);
  line-height: 1.75;
  font-weight: 400;
}
</style>
