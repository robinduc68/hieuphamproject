<template>
  <div class="news-page">
    <h1 class="news-title">BẢN TIN TƠ LỤA</h1>

    <p v-if="loading" class="news-empty">Đang tải bài viết...</p>
    <p v-else-if="!posts.length" class="news-empty">Chưa có bài viết nào.</p>

    <div v-else class="news-grid">
      <RouterLink
        v-for="post in posts"
        :key="post.id"
        :to="`/tin-tuc/${post.slug}`"
        class="news-card"
      >
        <div class="card-meta">
          <span v-if="post.tag" class="card-tag">
            <span class="tag-dot" />
            {{ post.tag }}
          </span>
          <span v-else />
          <span class="card-date">{{ formatDate(post.published_at) }}</span>
        </div>

        <div class="card-img-wrap">
          <div class="card-img" :style="{ background: post.cover_color || DEFAULT_BG }">
            <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" class="card-photo" />
          </div>
        </div>

        <div class="card-body">
          <h2 class="card-title">{{ post.title }}</h2>
          <p class="card-excerpt">{{ post.excerpt || post.subtitle }}</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postsApi } from '@/api'
import { formatPostDate, DEFAULT_POST_BG as DEFAULT_BG } from '@/utils/posts'

const posts   = ref([])
const loading = ref(true)

const formatDate = formatPostDate

onMounted(async () => {
  try {
    const data = await postsApi.list({ per_page: 48 })
    posts.value = data.results ?? []
  } catch (e) {
    console.error('[NewsView]', e)
    posts.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.news-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: var(--page-top) var(--page-x) 96px;
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
.card-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.news-empty {
  text-align: center;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-muted);
  padding: 40px 0 80px;
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

@media (max-width: 1024px) {
  .news-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
}
@media (max-width: 768px) {
  .news-page  { padding-bottom: 64px; }
  .news-title { font-size: 28px; letter-spacing: 2px; margin-bottom: 30px; }
}
@media (max-width: 560px) {
  .news-grid { grid-template-columns: 1fr; }
}
</style>
