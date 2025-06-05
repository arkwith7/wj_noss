import api from './api'

export async function getProcessingStatus() {
  return api.get('/processing/status')
}
