<template>
  <div id="app-root">
    <AppHeader :overlay="route.name === 'home'" />
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
    <AppFooter />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
const route = useRoute()
</script>

<style>
.page-enter-active,
.page-leave-active { transition: opacity .25s ease; }
.page-enter-from,
.page-leave-to { opacity: 0; }
</style>
