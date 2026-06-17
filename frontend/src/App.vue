<template>
  <div id="app-root">
    <AppHeader :overlay="true" />
    <div style="flex: 1">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </div>
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
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-enter-active,
.page-leave-active { transition: opacity .25s ease; }
.page-enter-from,
.page-leave-to { opacity: 0; }



</style>
