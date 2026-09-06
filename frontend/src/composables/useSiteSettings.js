import { ref } from 'vue'
import client from '@/api/client'

/**
 * Cấu hình nội dung admin sửa được (video trang chủ, bảng hướng dẫn chọn size,
 * bảng định mức may đo). Nạp một lần cho cả app — mọi component dùng chung
 * cùng một ref, không gọi API lặp lại.
 */
const settings = ref({})
const loaded   = ref(false)
let inflight   = null

export function useSiteSettings() {
  if (!loaded.value && !inflight) {
    inflight = client.get('/settings/')
      .then((r) => { settings.value = r.data ?? {}; loaded.value = true })
      .catch((e) => { console.error('[useSiteSettings]', e) })
      .finally(() => { inflight = null })
  }
  return { settings, loaded }
}

/** Bảng {columns, rows} + title/note, quay về mặc định nếu admin chưa cấu hình. */
export function guideTable(value, fallback) {
  const v = value ?? {}
  const columns = v.columns?.length ? v.columns : fallback.columns
  const rows    = v.rows?.length    ? v.rows    : fallback.rows
  return {
    title: v.title || fallback.title,
    note:  v.note ?? fallback.note,
    columns,
    rows,
  }
}
