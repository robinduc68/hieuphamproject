import client from './client'

export const ordersApi = {
  create(payload) {
    return client.post('/orders/', payload).then((r) => r.data)
  },
  myOrders() {
    return client.get('/orders/my-orders').then((r) => r.data)
  },
  detail(id) {
    return client.get(`/orders/${id}`).then((r) => r.data)
  },
}

export const paymentsApi = {
  /** Tạo (hoặc lấy lại) mã QR VietQR cho đơn hàng */
  vietqr(orderCode) {
    return client.post(`/payments/vietqr/${orderCode}`).then((r) => r.data)
  },
  /** Hỏi lại xem tiền đã về chưa */
  status(orderCode) {
    return client.get(`/payments/status/${orderCode}`).then((r) => r.data)
  },
}

export const newsletterApi = {
  subscribe(email, fullName) {
    return client
      .post('/newsletter/subscribe', { email, full_name: fullName })
      .then((r) => r.data)
  },
}
