import axios from 'axios'

// Danh mục hành chính Việt Nam (tỉnh/thành → phường/xã, mô hình 2 cấp từ 2025).
// Public API, không cần key: https://provinces.open-api.vn
const locationsClient = axios.create({
  baseURL: 'https://provinces.open-api.vn/api/v2',
  timeout: 10_000,
})

export const locationsApi = {
  /** Danh sách tỉnh / thành phố */
  provinces() {
    return locationsClient.get('/p/').then((r) => r.data)
  },
  /** Danh sách phường / xã thuộc 1 tỉnh / thành phố */
  wards(provinceCode) {
    return locationsClient
      .get(`/p/${provinceCode}`, { params: { depth: 2 } })
      .then((r) => r.data.wards ?? [])
  },
}