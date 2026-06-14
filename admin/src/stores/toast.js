import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let id = 0

  function show(message, type = 'success', duration = 3000) {
    const t = { id: ++id, message, type }
    toasts.value.push(t)
    setTimeout(() => { toasts.value = toasts.value.filter(x => x.id !== t.id) }, duration)
  }

  const success = (msg) => show(msg, 'success')
  const error   = (msg) => show(msg, 'error')

  return { toasts, success, error }
})
