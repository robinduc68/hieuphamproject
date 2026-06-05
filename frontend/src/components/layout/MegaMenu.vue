<template>
  <Transition name="mega">
    <div v-if="open" class="mega-menu" @mouseenter="$emit('keep')" @mouseleave="$emit('close')">
      <div class="mega-left">
        <div
          v-for="cat in categories"
          :key="cat.slug"
          class="mega-cat"
          :class="{ active: activeCat === cat.slug }"
          @mouseenter="activeCat = cat.slug"
          @click="navigate(cat); $emit('close')"
        >
          <span>{{ cat.label }}</span>
          <svg v-if="cat.subs.length" class="cat-arrow" viewBox="0 0 6 10" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M1 1l4 4-4 4"/>
          </svg>
        </div>
      </div>

      <div class="mega-right">
        <RouterLink
          v-for="sub in currentSubs"
          :key="sub.slug"
          :to="`/danh-muc/${sub.slug}`"
          class="mega-sub"
          @click="$emit('close')"
        >{{ sub.label }}</RouterLink>
        <p v-if="!currentSubs.length" class="mega-empty">Xem tất cả</p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  open:       { type: Boolean, default: false },
  categories: { type: Array,   default: () => [] },
})
defineEmits(['close', 'keep'])

const router = useRouter()
const activeCat = ref(props.categories[0]?.slug ?? '')

const directRoutes = { 'lua-to-tam': '/lua-to-tam' }

function navigate(cat) {
  const direct = directRoutes[cat.slug]
  if (direct) router.push(direct)
  else router.push(`/danh-muc/${cat.slug}`)
}

const currentSubs = computed(() => {
  const cat = props.categories.find(c => c.slug === activeCat.value)
  return cat?.subs ?? []
})
</script>

<style scoped>
.mega-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 500;
  display: flex;
  background: #fff;
  border: 1px solid var(--border);
  box-shadow: 0 12px 32px rgba(0,0,0,.14);
  min-width: 380px;
}

.mega-left {
  min-width: 200px;
  border-right: 1px solid var(--border);
  padding: 8px 0;
}

.mega-cat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 15px 28px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  color: var(--text-dark);
  cursor: pointer;
  white-space: nowrap;
  transition: background var(--transition), color var(--transition);
}
.mega-cat.active,
.mega-cat:hover {
  background: var(--brand-red);
  color: #fff;
}
.mega-cat.active .cat-arrow,
.mega-cat:hover .cat-arrow {
  stroke: #fff;
}

.cat-arrow {
  width: 6px;
  height: 10px;
  flex-shrink: 0;
  stroke: var(--text-muted);
  transition: stroke var(--transition);
}

.mega-right {
  padding: 8px 0;
  min-width: 240px;
}

.mega-sub {
  display: block;
  padding: 15px 32px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  color: var(--text-dark);
  white-space: nowrap;
  transition: color var(--transition), padding-left var(--transition);
}
.mega-sub:hover {
  color: var(--brand-red);
  padding-left: 38px;
}

.mega-empty {
  padding: 15px 32px;
  font-size: 15px;
  color: var(--text-muted);
  font-style: italic;
}

.mega-enter-active,
.mega-leave-active {
  transition: opacity .2s ease, transform .2s ease;
  transform-origin: top left;
}
.mega-enter-from,
.mega-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
