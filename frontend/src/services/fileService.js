import api from './api'

export async function getFileList() {
  return api.get('/files')
}
