// Dùng chung cho trang Tin tức và trang chi tiết bài viết.

/** Nền của ảnh bìa khi bài viết chưa có ảnh. */
export const DEFAULT_POST_BG = 'linear-gradient(135deg, #D8CFC0 0%, #C4B8A6 50%, #E0D7C8 100%)'

/** '2025-08-08' → '08/08/2025' */
export function formatPostDate(value) {
  if (!value) return ''
  const [y, m, d] = String(value).slice(0, 10).split('-')
  return d && m && y ? `${d}/${m}/${y}` : String(value)
}
