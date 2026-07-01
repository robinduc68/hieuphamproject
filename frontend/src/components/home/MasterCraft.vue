<template>
  <section class="craft-section">
    <div class="craft-head">
      <h2 class="craft-title">LỤA TƠ TẰM NHA XÁ - GỐC NGHỆ NHÂN</h2>
      <p class="craft-script">Tinh hoa trong từng sợi vải</p>
    </div>

    <div class="craft-cards">
      <div v-for="c in cards" :key="c.title" class="craft-card">
        <img class="craft-icon" :src="c.icon" :alt="c.title" />
        <h3 class="craft-card-title">{{ c.title }}</h3>
        <p class="craft-card-desc">{{ c.desc }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const cards = [
  {
    icon: '/1.png',   // vải → hoa văn → chỉ kim: quy trình sản xuất
    title: 'Dệt & Nhuộm thủ công tỉ mỉ',
    desc: 'Từng thước lụa mang trọn tâm huyết và kỹ nghệ truyền thống của làng nghề.',
  },
  {
    icon: '/6.png',   // vải gấp + tem chứng nhận: cam kết chất lượng
    title: 'Lựa chọn cao cấp',
    desc: 'Cam kết chất liệu tơ tằm Nha Xá cao cấp, dày dặn, đanh mướt, óng ả.',
  },
  {
    icon: '/7.png',   // nhiều lớp vải xếp chồng: đa dạng mẫu vải
    title: 'Kho vải đồ sộ 5000+ mẫu',
    desc: 'Luôn sẵn kho hàng ngàn màu sắc, họa tiết để bạn thỏa sức lựa chọn.',
  },
]
</script>

<style scoped>
.craft-section {
  background: var(--bg-gray);
  padding: 80px 48px;
}

.craft-head {
  text-align: center;
  margin-bottom: 48px;
}
.craft-title {
  font-family: 'Philosopher', sans-serif;
  font-size: 41.3px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--brand-red);
  line-height: 1.2;
}
.craft-script {
  font-family: var(--font-script);
  font-size: 46px;
  color: var(--brand-red);
  line-height: 1;
  margin-top: 6px;
}

.craft-cards {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.craft-card {
  background: #DEDEDE;
  border-radius: var(--radius);
  padding: 36px 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: box-shadow var(--transition), transform var(--transition);
}
.craft-card:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, .08);
  transform: translateY(-3px);
}

.craft-icon {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.craft-card-title {
  font-family: 'Philosopher', sans-serif;
  font-size: 22px;
  font-weight: 600;
  color: #681927;
  line-height: 1.3;
}

.craft-card-desc {
  font-size: 13px;
  color: var(--text-medium);
  line-height: 1.75;
}

@media (max-width: 860px) {
  .craft-cards { grid-template-columns: 1fr; }
}
</style>
