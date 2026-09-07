<template>
  <div class="faq-page">
    <h1 class="faq-title">{{ pageTitle }}</h1>

    <div class="faq-list">
      <div
        v-for="(item, i) in faqs"
        :key="i"
        class="faq-item"
      >
        <div class="faq-divider" />
        <button
          class="faq-trigger"
          :class="{ open: openIndex === i }"
          @click="openIndex = openIndex === i ? null : i"
        >
          <span class="faq-q">
            <span class="faq-num">{{ i + 1 }}.</span>
            {{ item.question }}
          </span>
          <svg
            class="faq-icon"
            :class="{ rotated: openIndex === i }"
            viewBox="0 0 24 14" fill="none"
            stroke="currentColor" stroke-width="1.8"
          >
            <path d="M2 12L12 2l10 10"/>
          </svg>
        </button>
        <Transition name="faq-body">
          <div v-if="openIndex === i" class="faq-answer">
            <p>{{ item.answer }}</p>
          </div>
        </Transition>
      </div>
      <div class="faq-divider" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSiteSettings } from '@/composables/useSiteSettings'

const openIndex = ref(0)

// Nội dung admin sửa trong trang admin → "Nội dung web" → "Câu hỏi thường gặp".
// Danh sách dưới đây chỉ là dự phòng khi API chưa trả về được cấu hình.
const FALLBACK = {
  title: 'CÂU HỎI THƯỜNG GẶP',
  items: [
    {
      question: 'Mất bao lâu để hoàn thành một sản phẩm may đo?',
      answer: 'Trung bình, quy trình may đo thủ công sẽ mất từ 1–2 tuần kể từ khi bạn chốt đơn hàng và đặt cọc. Mọi đường kim mũi chỉ đều cần tính toán tỉ mỉ để phù hợp với bạn nhất, Hà Hoạt Silk hy vọng bạn có thể kiên nhẫn chờ đợi tác phẩm của mình.',
    },
    {
      question: 'Tôi có thể đặt may theo số đo riêng không?',
      answer: 'Hoàn toàn có thể. Hà Hoạt Silk nhận may theo số đo cá nhân với đầy đủ các thông số: ngực, eo, hông, chiều dài tay, chiều cao. Bạn có thể tham khảo hướng dẫn lấy số đo trên trang hoặc liên hệ trực tiếp để được hỗ trợ.',
    },
    {
      question: 'Chính sách đổi trả như thế nào?',
      answer: 'Hà Hoạt Silk hỗ trợ đổi trả trong vòng 7 ngày kể từ ngày nhận hàng với điều kiện sản phẩm chưa qua sử dụng, còn nguyên tag và bao bì. Riêng sản phẩm may theo số đo cá nhân sẽ không áp dụng đổi trả, ngoại trừ trường hợp lỗi từ phía nhà sản xuất.',
    },
  ],
}

const { settings } = useSiteSettings()

const pageTitle = computed(() => settings.value.faq_page?.title || FALLBACK.title)

const faqs = computed(() => {
  const items = settings.value.faq_page?.items
  return Array.isArray(items) && items.length ? items : FALLBACK.items
})
</script>

<style scoped>
.faq-page {
  min-height: 80vh;
  background: var(--bg-gray);
  padding: 100px 48px 96px;
}

.faq-title {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 700;
  letter-spacing: 4px;
  color: var(--brand-red);
  text-align: center;
  margin-bottom: 56px;
}

.faq-list {
  max-width: 860px;
  margin: 0 auto;
}

.faq-divider {
  height: 1px;
  background: #D8D8D4;
}

.faq-trigger {
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: color var(--transition);
}

.faq-q {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 400;
  color: #999;
  line-height: 1.5;
  transition: color var(--transition), font-weight var(--transition);
  display: flex;
  gap: 10px;
}

.faq-trigger.open .faq-q {
  font-weight: 700;
  color: var(--charcoal);
}

.faq-num {
  flex-shrink: 0;
}

.faq-icon {
  width: 20px;
  height: 12px;
  flex-shrink: 0;
  margin-top: 4px;
  color: #999;
  transition: transform var(--transition), color var(--transition);
}
.faq-trigger.open .faq-icon {
  color: var(--charcoal);
}
.faq-icon.rotated {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 0 28px;
}
.faq-answer p {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.85;
  color: var(--text-dark);
  max-width: 820px;
  white-space: pre-line;   /* giữ ngắt dòng admin gõ trong ô trả lời */
}

.faq-body-enter-active,
.faq-body-leave-active {
  transition: max-height .3s ease, opacity .25s ease;
  overflow: hidden;
  max-height: 300px;
}
.faq-body-enter-from,
.faq-body-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
