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

export const newsletterApi = {
  subscribe(email, fullName) {
    return client
      .post('/newsletter/subscribe', { email, full_name: fullName })
      .then((r) => r.data)
  },
}
