/**
 * Địa chỉ web khách, để trang admin mở thẳng trang sản phẩm / bài viết.
 *
 * Thứ tự ưu tiên:
 *   1. VITE_SITE_URL (đặt trong .env khi build) — dùng khi domain không theo
 *      quy ước dưới đây.
 *   2. admin.<domain>  → <domain>          (production: admin.hahoatsilk.com → hahoatsilk.com)
 *   3. localhost/127.0.0.1 → cùng host, port 3000 (docker-compose dev)
 *   4. Cùng origin — trường hợp admin nằm chung domain với web.
 */
const DEV_SITE_PORT = '3000'

export function siteOrigin() {
  const configured = import.meta.env.VITE_SITE_URL
  if (configured) return String(configured).replace(/\/+$/, '')

  const { protocol, hostname, port } = window.location

  if (hostname.startsWith('admin.')) {
    return `${protocol}//${hostname.slice('admin.'.length)}${port && port !== '80' && port !== '443' ? `:${port}` : ''}`
  }
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return `${protocol}//${hostname}:${DEV_SITE_PORT}`
  }
  return window.location.origin
}

/** siteUrl('/san-pham/ao-dai') → 'https://hahoatsilk.com/san-pham/ao-dai' */
export function siteUrl(path = '/') {
  return siteOrigin() + (path.startsWith('/') ? path : `/${path}`)
}
