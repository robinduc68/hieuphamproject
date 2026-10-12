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

      <!-- Article: cột mục lục bên trái, nội dung bên phải -->
      <div class="nd-layout" :class="{ 'has-toc': toc.length > 1 }">


        <div class="nd-head">
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
        </div>

        <!-- Mục lục — tự sinh từ các tiêu đề trong bài -->
        <aside v-if="toc.length > 1" class="nd-toc" aria-label="Mục lục">
          <button class="toc-head" :aria-expanded="tocOpen" @click="tocOpen = !tocOpen">
            Mục lục
            <svg class="toc-caret" :class="{ open: tocOpen }" viewBox="0 0 12 8" fill="none"
                 stroke="currentColor" stroke-width="1.6"><path d="M1 1l5 5 5-5"/></svg>
          </button>
          <nav class="toc-list" :class="{ open: tocOpen }">
            <a
              v-for="item in toc"
              :key="item.id"
              :href="`#${item.id}`"
              class="toc-link"
              :class="[`lv-${item.level}`, { active: activeId === item.id }]"
              @click.prevent="goTo(item.id)"
            >{{ item.text }}</a>
          </nav>
        </aside>

        <div class="nd-body">
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
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { postsApi } from '@/api'
import { renderRichText } from '@/utils/richtext'
import { formatPostDate, DEFAULT_POST_BG as DEFAULT_BG } from '@/utils/posts'

const route = useRoute()

const post    = ref(null)
const related = ref([])
const loading = ref(true)

const formatDate = formatPostDate

// ── Mục lục ──────────────────────────────────────────────────────────────
// Tự sinh từ các tiêu đề trong bài, không bắt admin khai báo thêm gì.
const VI_MAP = {
  à:'a',á:'a',ả:'a',ã:'a',ạ:'a',ă:'a',ắ:'a',ằ:'a',ẳ:'a',ẵ:'a',ặ:'a',
  â:'a',ấ:'a',ầ:'a',ẩ:'a',ẫ:'a',ậ:'a',
  è:'e',é:'e',ẻ:'e',ẽ:'e',ẹ:'e',ê:'e',ế:'e',ề:'e',ể:'e',ễ:'e',ệ:'e',
  ì:'i',í:'i',ỉ:'i',ĩ:'i',ị:'i',
  ò:'o',ó:'o',ỏ:'o',õ:'o',ọ:'o',ô:'o',ố:'o',ồ:'o',ổ:'o',ỗ:'o',ộ:'o',
  ơ:'o',ớ:'o',ờ:'o',ở:'o',ỡ:'o',ợ:'o',
  ù:'u',ú:'u',ủ:'u',ũ:'u',ụ:'u',ư:'u',ứ:'u',ừ:'u',ử:'u',ữ:'u',ự:'u',
  ỳ:'y',ý:'y',ỷ:'y',ỹ:'y',ỵ:'y',đ:'d',
}
function slugify(text) {
  return String(text).toLowerCase()
    .split('').map(c => VI_MAP[c] ?? c).join('')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim().replace(/\s+/g, '-').replace(/-+/g, '-')
}

/** Gắn id vào từng tiêu đề rồi trả về cả HTML lẫn danh sách mục lục. */
const parsed = computed(() => {
  const html = renderRichText(post.value?.content)
  if (!html) return { html: '', toc: [] }

  const doc  = new DOMParser().parseFromString(`<body>${html}</body>`, 'text/html')
  const toc  = []
  const used = new Set()

  doc.body.querySelectorAll('h1, h2, h3').forEach((h) => {
    const text = h.textContent.trim()
    if (!text) return
    const base = slugify(text) || 'muc'
    let id = base
    for (let n = 2; used.has(id); n += 1) id = `${base}-${n}`
    used.add(id)
    h.id = id
    toc.push({ id, text, level: Number(h.tagName[1]) })
  })
  return { html: doc.body.innerHTML, toc }
})

const contentHtml = computed(() => parsed.value.html)
const toc         = computed(() => parsed.value.toc)

// Dưới ngưỡng này mục lục thành ô gập — phải khớp @media trong CSS
const TOC_SIDEBAR_MIN = 1360
const tocOpen  = ref(true)
const activeId = ref('')

// Header dính ~74px, chừa thêm cho thoáng
const SCROLL_OFFSET = 110

function goTo(id) {
  const el = document.getElementById(id)
  if (!el) return
  window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - SCROLL_OFFSET, behavior: 'smooth' })
  activeId.value = id
  if (window.innerWidth < TOC_SIDEBAR_MIN) tocOpen.value = false
}

let ticking = false
function onScroll() {
  if (ticking) return
  ticking = true
  requestAnimationFrame(() => {
    ticking = false
    const list = toc.value
    if (!list.length) return
    let current = list[0].id
    for (const item of list) {
      const el = document.getElementById(item.id)
      if (el && el.getBoundingClientRect().top <= SCROLL_OFFSET + 10) current = item.id
    }
    activeId.value = current
  })
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// Bài mới nạp xong mới có tiêu đề trong DOM → tính lại mục đang đọc
watch(toc, async (list) => {
  tocOpen.value  = window.innerWidth >= TOC_SIDEBAR_MIN
  activeId.value = list[0]?.id ?? ''
  await nextTick()
  onScroll()
})

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

/* Bố cục: mục lục bám bên trái, bài viết ở giữa */
.nd-layout {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 var(--page-x) 96px;
}
.nd-layout .nd-head,
.nd-layout .nd-body { max-width: 820px; margin: 0 auto; }

/* Từ 1360px trở lên: 3 cột, cột giữa là bài viết nên bài vẫn nằm CHÍNH GIỮA
   trang như cũ, mục lục chiếm lề trái chứ không đẩy bài sang phải.
   Hẹp hơn thì lề không đủ chỗ → mục lục thành ô gập ở dưới tiêu đề. */
@media (min-width: 1360px) {
  .nd-layout.has-toc {
    /* bỏ khung 1180px để 2 cột lề thật sự bằng nhau → bài nằm giữa màn hình */
    max-width: none;
    display: grid;
    /* minmax(0,1fr) để 2 cột lề co được: mục lục rộng bao nhiêu cũng không
       đẩy bài viết lệch khỏi giữa màn hình */
    grid-template-columns: minmax(0, 1fr) minmax(0, 820px) minmax(0, 1fr);
    align-items: start;
  }
  .nd-layout.has-toc .nd-head { grid-column: 2; grid-row: 1; }
  .nd-layout.has-toc .nd-body { grid-column: 2; grid-row: 2; }
  .nd-layout.has-toc .nd-toc  {
    grid-column: 1; grid-row: 1 / span 2;
    justify-self: end;
    width: 100%;
    max-width: 288px;     /* màn rộng thì tối đa 288, hẹp thì tự co lại */
    padding-right: 36px;
  }
}

/* ── Mục lục ── */
.nd-toc {
  position: sticky;
  top: 104px;
  padding-top: 24px;
}
.toc-head {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%;
  padding: 0 0 14px;
  background: none; border: none;
  border-bottom: 1px solid var(--border);
  font-family: var(--font-body);
  font-size: 22px; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--brand-red);
  cursor: default;
}
.toc-caret { display: none; width: 12px; height: 8px; transition: transform var(--transition); }

.toc-list {
  display: flex; flex-direction: column;
  max-height: calc(100vh - 210px);
  overflow-y: auto;
  padding: 12px 0 4px;
  scrollbar-width: thin;
}
.toc-list::-webkit-scrollbar { width: 3px; }
.toc-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.toc-link {
  position: relative;
  padding: 10px 0 10px 16px;
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-muted);
  border-left: 2px solid transparent;
  transition: color var(--transition), border-color var(--transition);
}
.toc-link:hover { color: var(--charcoal); }
.toc-link.active {
  color: var(--brand-red);
  font-weight: 600;
  border-left-color: var(--brand-red);
}
/* Tiêu đề con thụt vào cho thấy được thứ bậc */
.toc-link.lv-3 { padding-left: 30px; font-size: 14px; }

/* Màn hẹp: mục lục thành khối gập ở trên bài viết */
@media (max-width: 1359px) {
  .nd-toc {
    position: static;
    max-width: 820px;
    margin: 20px auto 0;
    padding: 14px 16px;
    background: var(--warm-white);
    border: 1px solid var(--border);
    border-radius: 10px;
  }
  .toc-head { padding-bottom: 0; border-bottom: none; cursor: pointer; }
  .toc-caret { display: block; }
  .toc-caret.open { transform: rotate(180deg); }
  .toc-list { display: none; max-height: none; padding-top: 10px; }
  .toc-list.open { display: flex; }
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
