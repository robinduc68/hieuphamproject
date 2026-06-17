<template>
  <div class="nd-page">

    <!-- Hero -->
    <div class="nd-hero" :style="{ background: post.imgBg }" />

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
          <span class="nd-tag">
            <span class="tag-dot" />
            {{ post.tag }}
          </span>
          <span class="nd-date">{{ post.date }}</span>
        </div>
        <h1 class="nd-title">{{ post.title }}</h1>
        <p class="nd-subtitle">{{ post.subtitle }}</p>
      </div>

      <!-- Content -->
      <article class="nd-content">
        <p class="nd-lead">{{ post.lead }}</p>

        <div v-for="(section, i) in post.sections" :key="i" class="nd-section">
          <h2 v-if="section.heading" class="nd-h2">{{ section.heading }}</h2>
          <p class="nd-p">{{ section.body }}</p>
          <div v-if="section.tips" class="nd-tips">
            <div v-for="tip in section.tips" :key="tip.num" class="nd-tip">
              <span class="tip-num">{{ tip.num }}</span>
              <div>
                <strong class="tip-title">{{ tip.title }}</strong>
                <p class="tip-body">{{ tip.body }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="nd-quote">
          <blockquote>{{ post.quote }}</blockquote>
        </div>

        <p class="nd-p">{{ post.closing }}</p>
      </article>

      <!-- Tags -->
      <div class="nd-tags">
        <span v-for="t in post.tags" :key="t" class="nd-chip">{{ t }}</span>
      </div>

      <!-- Divider -->
      <div class="nd-divider" />

      <!-- Related -->
      <section class="nd-related">
        <h3 class="related-title">Bài viết liên quan</h3>
        <div class="related-grid">
          <RouterLink
            v-for="rel in related"
            :key="rel.id"
            :to="`/tin-tuc/${rel.slug}`"
            class="related-card"
          >
            <div class="related-img" :style="{ background: rel.imgBg }" />
            <div class="related-body">
              <span class="related-tag">
                <span class="tag-dot" />{{ rel.tag }}
              </span>
              <p class="related-title-text">{{ rel.title }}</p>
              <span class="related-date">{{ rel.date }}</span>
            </div>
          </RouterLink>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const allPosts = [
  {
    id: 1, slug: 'da-ngam-hop-voi-mau-gi',
    tag: 'Tips mặc đẹp', date: '08/08/2025',
    imgBg: 'linear-gradient(135deg, #C8A898 0%, #B08878 50%, #D0B0A0 100%)',
    title: 'Da ngăm hợp với màu gì? 7 gam màu "cứ mặc là đẹp"',
    subtitle: 'Khám phá bảng màu được các chuyên gia thời trang gợi ý dành riêng cho tông da ngăm — đẹp tự nhiên, không cần cố.',
    lead: 'Da ngăm vốn được ví như "vàng nâu" của người Việt — ấm áp, khỏe khoắn và đậm chất nhiệt đới. Thế nhưng nhiều người vẫn loay hoay không biết chọn màu sắc như thế nào để tôn lên làn da này. Dưới đây là 7 gam màu mà các chuyên gia phong cách khuyên bạn nên thử.',
    sections: [
      {
        heading: '1. Màu trắng ngà (off-white)',
        body: 'Không phải trắng tinh, mà là trắng kem hoặc trắng ngà mới là lựa chọn hoàn hảo. Gam màu này tạo ra sự tương phản nhẹ nhàng, làm nổi bật làn da ngăm mà không gây cảm giác "lạc lõng".',
      },
      {
        heading: '2. Vàng đất & caramel',
        body: 'Các tông vàng ấm như caramel, vàng mustard hay vàng đất đều cực kỳ hợp với da ngăm. Chúng cùng hệ màu ấm nên hòa hợp tự nhiên, tạo cảm giác gương mặt rạng rỡ hơn.',
        tips: [
          { num: '01', title: 'Vàng mustard', body: 'Đậm, cá tính — hợp với áo dài cách điệu.' },
          { num: '02', title: 'Caramel nhạt', body: 'Thanh lịch, phù hợp với áo dài truyền thống.' },
          { num: '03', title: 'Vàng đất', body: 'Gần với màu đất nung, đậm chất Á Đông.' },
        ],
      },
      {
        heading: '3. Đỏ rượu & đỏ gạch',
        body: 'Đây là bộ đôi "không bao giờ sai" cho làn da ngăm. Đỏ rượu tạo nên vẻ sang trọng, huyền bí; đỏ gạch mang lại cảm giác ấm áp, gần gũi nhưng vẫn đủ nổi bật.',
      },
      {
        heading: '4. Xanh cổ vịt & xanh ngọc',
        body: 'Các tông xanh lạnh khi chạm vào da ngăm lại tạo ra hiệu ứng tương phản rất đẹp mắt. Xanh cổ vịt hay xanh ngọc đều mang lại vẻ thanh thoát, hiện đại cho người mặc.',
      },
      {
        heading: '5. Cam san hô',
        body: 'Cam san hô — màu xu hướng nhiều năm liền — là người bạn đồng hành lý tưởng của làn da ngăm. Màu này "ăn" với da ngăm theo cách không một gam màu nào sánh được.',
      },
      {
        heading: '6. Hồng đất & hồng nâu',
        body: 'Hồng đất (mauve) hay hồng nâu (dusty rose) là những gam màu tinh tế, không quá chói, tôn lên vẻ nữ tính mà vẫn giữ được nét thanh lịch đặc trưng của áo dài.',
      },
      {
        heading: '7. Tím mận & tím eggplant',
        body: 'Cuối danh sách nhưng không hề kém cạnh — tím mận và tím tối mang lại vẻ quý phái, bí ẩn. Khi kết hợp với chất liệu lụa tơ tằm có ánh nhũ, hiệu ứng đẹp đến khó tin.',
      },
    ],
    quote: '"Màu sắc là ngôn ngữ riêng của áo dài — mỗi gam màu kể một câu chuyện khác nhau về người mặc nó."',
    closing: 'Dù bạn chọn gam màu nào, điều quan trọng nhất vẫn là sự tự tin của người mặc. Hà Hoạt Silk luôn sẵn sàng tư vấn và đồng hành cùng bạn trên hành trình tìm kiếm bộ áo dài ưng ý nhất.',
    tags: ['Tips mặc đẹp', 'Màu sắc', 'Áo dài', 'Phong cách'],
  },
  {
    id: 2, slug: 'cach-chon-vai-lua-chuan',
    tag: 'Kiến thức vải', date: '01/08/2025',
    imgBg: 'linear-gradient(135deg, #A8B8C8 0%, #8898A8 50%, #B8C8D8 100%)',
    title: 'Cách chọn vải lụa chuẩn — không bị "hớ" khi mua online',
    subtitle: 'Phân biệt lụa tơ tằm thật với các loại vải giả lụa tràn lan trên thị trường.',
    lead: 'Thị trường vải hiện nay vô cùng đa dạng, khiến không ít người khó phân biệt lụa thật và lụa giả. Bài viết này sẽ giúp bạn trang bị những kiến thức cần thiết.',
    sections: [],
    quote: '"Lụa thật không bao giờ cần quảng cáo — chất liệu tự nói lên tất cả."',
    closing: 'Khi mua vải lụa, hãy luôn yêu cầu thông tin xuất xứ và chứng nhận chất lượng từ nhà cung cấp.',
    tags: ['Kiến thức vải', 'Lụa tơ tằm', 'Mua sắm'],
  },
  {
    id: 3, slug: 'ao-dai-cho-mua-cuoi',
    tag: 'Xu hướng', date: '25/07/2025',
    imgBg: 'linear-gradient(135deg, #D4C8A8 0%, #C4B890 50%, #D8C8A8 100%)',
    title: 'Áo dài cho mùa cưới 2025 — xu hướng màu sắc và họa tiết',
    subtitle: 'Điểm qua những thiết kế áo dài đang được săn đón nhất trong mùa cưới năm nay.',
    lead: 'Mùa cưới 2025 đang đến gần với những xu hướng áo dài mới mẻ, kết hợp giữa truyền thống và hiện đại.',
    sections: [],
    quote: '"Áo dài cưới không chỉ là trang phục — đó là ký ức được dệt bằng lụa."',
    closing: 'Liên hệ với Hà Hoạt Silk để được tư vấn và may bộ áo dài cưới hoàn hảo nhất.',
    tags: ['Xu hướng', 'Áo dài cưới', '2025'],
  },
]

const post = computed(() => {
  const found = allPosts.find(p => p.slug === route.params.slug)
  return found ?? allPosts[0]
})

const related = computed(() =>
  allPosts.filter(p => p.slug !== route.params.slug).slice(0, 2)
)
</script>

<style scoped>
.nd-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding-top: 100px;
}

/* Wrap */
.nd-wrap {
  max-width: 820px;
  margin: 0 auto;
  padding: 0 24px 96px;
}

/* Hero */
.nd-hero {
  max-width: 820px;
  margin: 32px auto 0;
  padding: 0 24px;
  height: 420px;
  border-radius: 14px;
}

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

.nd-lead {
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.9;
  color: var(--text-dark);
  font-weight: 500;
  margin-bottom: 36px;
}

.nd-section { margin-bottom: 32px; }

.nd-h2 {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 700;
  color: var(--charcoal);
  margin-bottom: 10px;
}

.nd-p {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.9;
  color: var(--text-dark);
}

/* Tips list */
.nd-tips {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 16px;
  padding-left: 8px;
}
.nd-tip {
  display: flex;
  gap: 18px;
  align-items: flex-start;
}
.tip-num {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 300;
  color: var(--brand-red);
  opacity: .5;
  line-height: 1;
  flex-shrink: 0;
  width: 28px;
  text-align: right;
}
.tip-title {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 700;
  color: var(--charcoal);
  display: block;
  margin-bottom: 3px;
}
.tip-body {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.65;
}

/* Quote */
.nd-quote {
  margin: 40px 0;
  padding: 24px 32px;
  border-left: 3px solid var(--brand-red);
  background: var(--cream);
}
.nd-quote blockquote {
  font-family: var(--font-display);
  font-size: 19px;
  font-style: italic;
  font-weight: 400;
  color: var(--charcoal);
  line-height: 1.7;
}

/* Tags */
.nd-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 40px;
}
.nd-chip {
  padding: 5px 14px;
  border: 1px solid var(--border);
  border-radius: 999px;
  font-family: var(--font-body);
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--text-muted);
  cursor: pointer;
  transition: border-color var(--transition), color var(--transition);
}
.nd-chip:hover { border-color: var(--brand-red); color: var(--brand-red); }

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
}

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
</style>
