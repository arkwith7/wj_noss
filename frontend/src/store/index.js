import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const sidebarOpen = ref(false)
  const theme = ref(localStorage.getItem('theme') || 'light')
  const notifications = ref([])
  const loading = ref(false)

  // Actions
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const closeSidebar = () => {
    sidebarOpen.value = false
  }

  const setTheme = (newTheme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    document.documentElement.classList.toggle('dark', newTheme === 'dark')
  }

  const addNotification = (notification) => {
    const id = Date.now()
    notifications.value.push({
      id,
      ...notification,
      timestamp: new Date()
    })
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      removeNotification(id)
    }, 5000)
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const setLoading = (isLoading) => {
    loading.value = isLoading
  }

  // Initialize theme
  document.documentElement.classList.toggle('dark', theme.value === 'dark')

  return {
    // State
    sidebarOpen,
    theme,
    notifications,
    loading,
    
    // Actions
    toggleSidebar,
    closeSidebar,
    setTheme,
    addNotification,
    removeNotification,
    setLoading
  }
})

export const useMainStore = defineStore('main', {
  state: () => ({
    uploadStatus: null,
    processingStatus: null,
    files: [],
  }),
  actions: {
    setUploadStatus(status) { this.uploadStatus = status },
    setProcessingStatus(status) { this.processingStatus = status },
    setFiles(files) { this.files = files },
  },
})
