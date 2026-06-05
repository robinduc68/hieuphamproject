import { ref } from 'vue'
import { collectionsApi } from '@/api'

export function useCollections() {
  const collections = ref([])
  const loading     = ref(false)
  const error       = ref(null)

  async function fetch() {
    loading.value = true
    error.value   = null
    try {
      collections.value = await collectionsApi.list()
    } catch (e) {
      error.value = 'Không thể tải bộ sưu tập.'
    } finally {
      loading.value = false
    }
  }

  fetch()
  return { collections, loading, error, fetch }
}
