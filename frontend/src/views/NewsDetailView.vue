<template>
  <div class="nd-page">
    <div v-if="loading" class="nd-state">Đang tải bài viết...</div>
    <div v-else-if="!post" class="nd-state">
      Không tìm thấy bài viết.
      <RouterLink to="/tin-tuc" class="nd-back">← Về trang Tin tức</RouterLink>
    </div>

    <template v-else>
      <!-- Hero -->
      <div class="nd-hero" :style="{ background: post.cover_color || DEFAULT_BG }">
        <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" class="nd-hero-photo" />
      </div>

      <!-- Article -->
      <div class="nd-wrap">

        <!-- Breadcrumb -->
        <nav class="nd-breadcrumb">
          <RouterLink to="/">Trang chủ</RouterLink>
          <span class="sep">/</span>
          <RouterLink to="/tin-tuc">Tin tức</RouterLink>
          <span class="sep">/</span>
          <span>{{ post.title }}</span>
        </nav>

        <!-- Header -->
        <div class="nd-header">
          <div class="nd-meta">
            <span v-if="post.tag" class="nd-tag">
              <span class="tag-dot" />
              {{ post.tag }}
            </span>
            <span class="nd-date">{{ formatDate(post.published_at) }}</span>
          </div>
          <h1 class="nd-title">{{ post.title }}</h1>
          <p v-if="post.subtitle" class="nd-subtitle">{{ post.subtitle }}</p>
        </div>

        <!-- Content -->
        <article class="nd-content rich-text" v-html="contentHtml" />

        <!-- Divider -->
        <div class="nd-divider" />

        <!-- Related -->
        <section v-if="related.length" class="nd-related">
          <h3 class="related-title">Bài viết liên quan</h3>
          <div class="related-grid">
            <RouterLink
              v-for="rel in related"
              :key="rel.id"
              :to="`/tin-tuc/${rel.slug}`"
              class="related-card"
            >
              <div class="related-img" :style="{ background: rel.cover_color || DEFAULT_BG }">
                <img v-if="rel.cover_image" :src="rel.cover_image" :alt="rel.title" class="related-photo" />
              </div>
              <div class="related-body">
                <span v-if="rel.tag" class="related-tag">
                  <span class="tag-dot" />{{ rel.tag }}
                </span>
                <p class="related-title-text">{{ rel.title }}</p>
                <span class="related-date">{{ formatDate(rel.published_at) }}</span>
              </div>
            </RouterLink>
          </div>
        </section>

      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { postsApi } from '@/api'
import { renderRichText } from '@/utils/richtext'
import { formatPostDate, DEFAULT_POST_BG as DEFAULT_BG } from '@/utils/posts'

const route = useRoute()

const post    = ref(null)
const related = ref([])
const loading = ref(true)

const formatDate  = formatPostDate
const contentHtml = computed(() => renderRichText(post.value?.content))

async function load(slug) {
  if (!slug) return
  loading.value = true
  try {
    post.value = await postsApi.detail(slug)
    related.value = await postsApi.related(slug, 2).catch(() => [])
  } catch (e) {
    console.error('[NewsDetailView]', e)
    post.value    = null
    related.value = []
  } finally {
    loading.value = false
  }
}

watch(() => route.params.slug, load, { immediate: true })
</script>

<style scoped>
.nd-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding-top: var(--page-top);
}

/* Wrap */
.nd-wrap {
  max-width: 820px;
  margin: 0 auto;
  padding: 0 var(--page-x) 96px;
}

/* Hero */
.nd-hero {
  max-width: 820px;
  margin: 32px auto 0;
  height: 420px;
  border-radius: 14px;
  overflow: hidden;
}
.nd-hero-photo { width: 100%; height: 100%; object-fit: cover; display: block; }

.nd-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 24px 120px;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-muted);
}
.nd-back { color: var(--brand-red); }

/* Breadcrumb */
.nd-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px 0 32px;
  font-family: var(--font-body);
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
}
.nd-breadcrumb a { color: var(--text-muted); transition: color var(--transition); }
.nd-breadcrumb a:hover { color: var(--brand-red); }
.sep { opacity: .4; }

/* Header */
.nd-header { margin-bottom: 40px; }

.nd-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}
.nd-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  color: var(--brand-red);
}
.tag-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--brand-red);
  flex-shrink: 0;
}
.nd-date {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-muted);
}

.nd-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 700;
  color: var(--charcoal);
  line-height: 1.3;
  margin-bottom: 14px;
}

.nd-subtitle {
  font-family: var(--font-display);
  font-size: 17px;
  font-style: italic;
  color: var(--text-muted);
  line-height: 1.7;
}

/* Content */
.nd-content { margin-bottom: 40px; }

.nd-divider {
  height: 1px;
  background: var(--border);
  margin-bottom: 48px;
}

/* Related */
.nd-related {}
.related-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 24px;
  letter-spacing: 1px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.related-card {
  display: flex;
  gap: 16px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  padding: 14px;
  transition: box-shadow var(--transition), transform var(--transition);
  color: inherit;
}
.related-card:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,.09);
  transform: translateY(-2px);
}

.related-img {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  flex-shrink: 0;
  overflow: hidden;
}
.related-photo { width: 100%; height: 100%; object-fit: cover; display: block; }

.related-body {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.related-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: var(--brand-red);
  font-family: var(--font-body);
}
.related-title-text {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: var(--charcoal);
  line-height: 1.4;
}
.related-date {
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--font-body);
}

@media (max-width: 768px) {
  .nd-hero  { height: 220px; margin-top: 18px; border-radius: 10px; }
  .nd-breadcrumb { padding: 16px 0 22px; font-size: 10px; gap: 6px; flex-wrap: wrap; }
  .nd-title { font-size: 24px; }
  .nd-subtitle { font-size: 15px; }
  .nd-header { margin-bottom: 28px; }
  .nd-divider { margin-bottom: 32px; }
  .related-grid { grid-template-columns: 1fr; }
  .related-title { font-size: 19px; }
}
</style>
