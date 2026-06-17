<template>
  <div class="news-page">
    <h1 class="news-title">BẢN TIN TƠ LỤA</h1>

    <div class="news-grid">
      <RouterLink
        v-for="post in posts"
        :key="post.id"
        :to="`/tin-tuc/${post.slug}`"
        class="news-card"
      >
        <div class="card-meta">
          <span class="card-tag">
            <span class="tag-dot" />
            {{ post.tag }}
          </span>
          <span class="card-date">{{ post.date }}</span>
        </div>

        <div class="card-img-wrap">
          <div class="card-img" :style="{ background: post.imgBg }" />
        </div>

        <div class="card-body">
          <h2 class="card-title">{{ post.title }}</h2>
          <p class="card-excerpt">{{ post.excerpt }}</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
const posts = [
  {
    id: 1,
    slug: 'da-ngam-hop-voi-mau-gi',
    tag: 'Tips mặc đẹp',
    date: '08/08/2025',
    title: 'Da ngăm hợp với màu gì? 7 gam màu "cứ mặc là đẹp"',
    excerpt: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non iaculis est...',
    imgBg: 'linear-gradient(135deg, #C8A898 0%, #B89888 50%, #D0B0A0 100%)',
  },
  {
    id: 2, slug: 'cach-chon-vai-lua-chuan',
    tag: 'Kiến thức vải', date: '01/08/2025',
    title: 'Cách chọn vải lụa chuẩn — không bị "hớ" khi mua online',
    excerpt: 'Phân biệt lụa tơ tằm thật với các loại vải giả lụa tràn lan trên thị trường hiện nay...',
    imgBg: 'linear-gradient(135deg, #A8B8C8 0%, #8898A8 50%, #B8C8D8 100%)',
  },
  {
    id: 3, slug: 'ao-dai-cho-mua-cuoi',
    tag: 'Xu hướng', date: '25/07/2025',
    title: 'Áo dài cho mùa cưới 2025 — xu hướng màu sắc và họa tiết',
    excerpt: 'Điểm qua những thiết kế áo dài đang được săn đón nhất trong mùa cưới năm nay...',
    imgBg: 'linear-gradient(135deg, #D4C8A8 0%, #C4B890 50%, #D8C8A8 100%)',
  },
  {
    id: 4, slug: 'bao-quan-ao-dai-lua',
    tag: 'Chăm sóc', date: '18/07/2025',
    title: 'Bí quyết bảo quản áo dài lụa bền đẹp qua năm tháng',
    excerpt: 'Những lưu ý quan trọng giúp áo dài lụa tơ tằm luôn giữ được độ bóng và form dáng...',
    imgBg: 'linear-gradient(135deg, #C8D0A8 0%, #B8C098 50%, #D0D8B0 100%)',
  },
  {
    id: 5, slug: 'lua-to-tam-va-suc-khoe',
    tag: 'Kiến thức vải', date: '10/07/2025',
    title: 'Lụa tơ tằm và sức khoẻ — lý do người xưa chuộng dùng',
    excerpt: 'Khoa học hiện đại chứng minh lụa tơ tằm có nhiều lợi ích vượt trội cho làn da...',
    imgBg: 'linear-gradient(135deg, #D0B8C8 0%, #C0A0B0 50%, #D8C0C8 100%)',
  },
  {
    id: 6, slug: 'phong-cach-ao-dai-hien-dai',
    tag: 'Phong cách', date: '02/07/2025',
    title: 'Phong cách áo dài hiện đại — giữa giữ hồn và đổi mới',
    excerpt: 'Áo dài đang được tái sinh với ngôn ngữ thiết kế mới mà vẫn giữ được bản sắc dân tộc...',
    imgBg: 'linear-gradient(135deg, #B8C8D8 0%, #A0B0C0 50%, #C0D0E0 100%)',
  },
]
</script>

<style scoped>
.news-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: 100px 80px 96px;
}

.news-title {
  font-family: var(--font-display);
  font-size: 40px;
  font-weight: 700;
  letter-spacing: 4px;
  color: var(--brand-red);
  text-align: center;
  margin-bottom: 48px;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  max-width: 1200px;
  margin: 0 auto;
}

.news-card {
  background: #fff;
  border: 1px solid #E0DED8;
  border-radius: 14px;
  overflow: hidden;
  padding: 16px 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  cursor: pointer;
  color: inherit;
  text-decoration: none;
  transition: box-shadow var(--transition), transform var(--transition);
}
.news-card:hover {
  box-shadow: 0 8px 28px rgba(0,0,0,.10);
  transform: translateY(-3px);
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-dark);
}

.tag-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-red);
  flex-shrink: 0;
}

.card-date {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-muted);
}

.card-img-wrap {
  border-radius: 10px;
  overflow: hidden;
}

.card-img {
  width: 100%;
  aspect-ratio: 4 / 3;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-title {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 700;
  color: var(--charcoal);
  line-height: 1.45;
}

.card-excerpt {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.65;
}
</style>
