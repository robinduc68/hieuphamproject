<template>
  <section class="custom-section">
    <div class="custom-inner">

      <!-- Top row: script title + heading -->
      <div class="custom-top">
        <p class="custom-script">Custom-Made</p>
        <h2 class="custom-heading">
          Để Hà Hoạt Silk giúp bạn <em><strong>tự tay</strong></em> tạo nên
          kiệt tác <span class="heading-accent"><em><strong>độc bản</strong></em></span>.
        </h2>
      </div>

      <!-- 4 steps -->
      <div class="steps">
        <div v-for="(step, index) in steps" :key="step.num" class="step" :style="{ marginTop: index * 28 + 'px' }">
          <span class="step-num">{{ step.num }}</span>
          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-desc">{{ step.desc }}</p>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    num: '01',
    title: 'Chọn mẫu áo dài, pháp phục',
    desc: 'Lựa chọn mẫu theo sở thích',
  },
  {
    num: '02',
    title: 'Điều chỉnh các tùy chọn',
    desc: 'Cân nhắc các lựa chọn hình thức may, kiểu dáng, phối màu',
  },
  {
    num: '03',
    title: '"Custom" thiết kế của riêng bạn',
    desc: 'Thay đổi mẫu vải nếu có nhu cầu để tạo ra thiết kế độc bản chỉ riêng bạn có.',
  },
  {
    num: '04',
    title: 'Sản phẩm được chế tác',
    desc: 'Hà Hoạt Silk giúp bạn hoàn thiện sản phẩm mang dấu ấn riêng.',
  },
]
</script>

<style scoped>
.custom-section {
  background: var(--bg-gray);
  padding: 80px 48px;
}

.custom-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 52px;
}

/* Top row */
.custom-top {
  display: grid;
  grid-template-columns: 220px 1fr;
  align-items: flex-start;
  gap: 56px;
  padding-top: 8px;
}

.custom-script {
  font-family: var(--font-script);
  font-size: 62px;
  color: var(--brand-red);
  line-height: 1.1;
}

.custom-heading {
  font-family: var(--font-display);
  font-size: 46px;
  font-weight: 400;
  color: var(--text-dark);
  line-height: 1.4;
}

.custom-heading strong {
  font-weight: 700;
}

.heading-accent {
  color: var(--brand-red);
}

/* Steps row */
.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  align-items: start;
}

.step {
  background: #E2E1DE;
  border-radius: 12px;
  padding: 36px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.step-num {
  font-family: var(--font-display);
  font-style: italic;
  font-size: 72px;
  font-weight: 300;
  color: var(--text-light);
  line-height: 1;
}

.step-title {
  font-family: var(--font-display);
  font-size: 19px;
  font-weight: 700;
  color: var(--brand-red);
  line-height: 1.4;
}

.step-desc {
  font-size: 14px;
  color: var(--text-medium);
  line-height: 1.7;
  font-weight: 400;
}
</style>
