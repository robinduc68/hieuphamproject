<template>
  <section class="custom-section">
    <div class="custom-inner">

      <!-- Top: 2-line centered heading -->
      <div class="custom-top">
        <h2 class="custom-heading">THIẾT KẾ TRANG PHỤC ĐỘC BẢN</h2>
        <p class="custom-sub">Trải nghiệm Custom-Made</p>
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
  background: #DEDEDE;
  padding: 80px 48px;
  color: rgb(104, 25, 39);
}

.custom-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 52px;
}

/* Top: centered 2-line heading */
.custom-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
  padding-top: 8px;
}

.custom-heading {
  font-family: 'Philosopher', sans-serif;
  font-size: 46px;
  color: rgb(104, 25, 39);
  line-height: 1.3;
}

.custom-sub {
  font-family: var(--font-script);
  font-size: 46px;
  color: rgb(104, 25, 39);
  line-height: 1.2;
}

/* Steps row */
.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  align-items: start;
}

.step {
  background: #ffffff;
  border-radius: 12px;
  padding: 36px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.step-num {
  font-family: var(--font-script);
  font-size: 72px;
  color: rgb(104, 25, 39);
  line-height: 1;
}

.step-title {
  font-family: 'Philosopher', sans-serif;
  font-size: 25px;
  color: rgb(104, 25, 39);
  line-height: 1.4;
}

.step-desc {
  font-size: 14px;
  color: #000000;
  line-height: 1.7;
  font-weight: 400;
}
</style>
