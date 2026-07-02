import client from './client.js'

export const customizationApi = {
  listGrouped: () => client.get('/customization-options/'),
}
