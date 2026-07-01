<template>
  <component
    :is="linked ? 'RouterLink' : 'div'"
    v-bind="linked ? { to: '/' } : {}"
    class="brand-logo"
    :class="`brand-logo--${size}`"
  >
    <!-- dark bg → cream logo, light bg → plum logo -->
    <img :src="dark ? '/HHS LG (1) (2).png' : '/HHSLG.png'" alt="Hà Hoạt Silk" class="logo-img" />
  </component>
</template>

<script setup>
defineProps({
  size:   { type: String, default: 'md' },
  linked: { type: Boolean, default: true },
  dark:   { type: Boolean, default: false },
})
</script>

<style scoped>
.brand-logo {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  user-select: none;
}

.logo-img {
  display: block;
  width: auto;
  height: 100%;
  object-fit: contain;
}

.brand-logo--sm  { height: 54px; margin-top: 6px; }
.brand-logo--md  { height: 64px; }
.brand-logo--lg  { height: 90px; }
</style>
