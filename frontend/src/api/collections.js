import client from './client'

export const collectionsApi = {
  list() {
    return client.get('/collections/').then((r) => r.data)
  },
  detail(slug) {
    return client.get(`/collections/${slug}`).then((r) => r.data)
  },
}
