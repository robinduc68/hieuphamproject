<template>
  <RouterView />
  <!-- Global toasts -->
  <div class="toast-wrap">
    <div
      v-for="t in toastStore.toasts"
      :key="t.id"
      class="toast"
      :class="`toast-${t.type}`"
    >
      <span v-if="t.type === 'success'">✓</span>
      <span v-else>✕</span>
      {{ t.message }}
    </div>
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast.js'
const toastStore = useToastStore()
</script>
