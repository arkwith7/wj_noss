import { ref } from 'vue'
import { getProcessingStatus } from '../services/processingService'

export function useProcessing() {
  const status = ref('')
  const progress = ref(0)
  let ws = null

  function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8000/api/v1/ws')
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      status.value = data.status
      progress.value = data.progress
    }
    ws.onclose = () => {
      // Optionally reconnect
    }
  }

  return { status, progress, connectWebSocket }
}
