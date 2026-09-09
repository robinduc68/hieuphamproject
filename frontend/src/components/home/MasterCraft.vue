<template>
  <section class="craft-section">
    <div class="craft-head">
      <h2 class="craft-title">LỤA TƠ TẰM NHA XÁ - GỐC NGHỆ NHÂN</h2>
      <p class="craft-script">Tinh hoa trong từng sợi vải</p>
    </div>

    <div class="craft-cards">
      <div v-for="c in cards" :key="c.title" class="craft-card">
        <img class="craft-icon" :src="c.icon" :alt="c.title" />
        <h3 class="craft-card-title" v-typewriter="24">{{ c.title }}</h3>
        <p class="craft-card-desc" v-typewriter="24">{{ c.desc }}</p>
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
  padding: var(--section-y) var(--page-x) 48px;   /* khớp padding ngang 20px; lùi đáy cho sát NewArrivals */
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
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 64px;           /* = nút 48px + gap 16px → căn đúng mép ảnh lụa (bỏ 2 nút) */
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.craft-card {
  background: #DEDEDE;
  border-radius: var(--radius);
  padding: 46px 28px 64px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  gap: 16px;
  transition: box-shadow var(--transition), transform var(--transition);
}
.craft-card:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, .08);
  transform: translateY(-3px);
}

.craft-icon {
  width: 90px;
  height: 90px;
  object-fit: contain;
}

.craft-card-title {
  font-family: 'Philosopher', sans-serif;
  font-size: 26px;
  font-weight: 600;
  color: #681927;
  line-height: 1.3;
  overflow-wrap: break-word;
}

.craft-card-desc {
  font-size: 15.5px;
  color: var(--text-medium);
  line-height: 1.75;
  overflow-wrap: break-word;
}

@media (max-width: 860px) {
  .craft-cards { grid-template-columns: 1fr; }
}
@media (max-width: 700px) {
  .craft-cards { margin: 0; }
}

@media (max-width: 560px) {
  .craft-card { padding: 30px 20px 40px; }
}
</style>
