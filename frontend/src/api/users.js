import client from './client'

export const usersApi = {
  register(payload) {
    return client.post('/users/register', payload).then((r) => r.data)
  },
  login(email, password) {
    return client.post('/users/login', { email, password }).then((r) => r.data)
  },
  me() {
    return client.get('/users/me').then((r) => r.data)
  },
  updateMe(payload) {
    return client.put('/users/me', payload).then((r) => r.data)
  },
  changePassword(oldPassword, newPassword) {
    return client
      .put('/users/me/password', null, {
        params: { old_password: oldPassword, new_password: newPassword },
      })
      .then((r) => r.data)
  },
}
