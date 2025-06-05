<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Activity History</h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            View and manage your document processing and AI interaction history.
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Filter Dropdown -->
          <div class="relative">
            <select
              v-model="selectedFilter"
              @change="applyFilter"
              class="block w-40 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="all">All Activities</option>
              <option value="documents">Documents</option>
              <option value="chats">AI Chats</option>
              <option value="templates">Templates</option>
            </select>
          </div>
          <!-- Date Range -->
          <div class="flex items-center space-x-2">
            <input
              v-model="dateRange.start"
              type="date"
              class="block px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <span class="text-gray-500 dark:text-gray-400">to</span>
            <input
              v-model="dateRange.end"
              type="date"
              class="block px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg">
              <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Documents</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ totalStats.documents }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 dark:bg-green-900/50 rounded-lg">
              <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">AI Chats</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ totalStats.chats }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div class="flex items-center">
            <div class="p-2 bg-purple-100 dark:bg-purple-900/50 rounded-lg">
              <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Templates</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ totalStats.templates }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div class="flex items-center">
            <div class="p-2 bg-orange-100 dark:bg-orange-900/50 rounded-lg">
              <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Tokens Used</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ totalStats.tokensUsed.toLocaleString() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Activity Timeline -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-medium text-gray-900 dark:text-white">Activity Timeline</h2>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Loading history...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredActivities.length === 0" class="p-8 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No activities found</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ selectedFilter === 'all' ? 'Start by uploading a document or creating a chat.' : `No ${selectedFilter} activities found.` }}
          </p>
        </div>

        <!-- Activity List -->
        <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
          <div
            v-for="activity in paginatedActivities"
            :key="activity.id"
            class="p-6 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
          >
            <div class="flex items-start space-x-4">
              <!-- Activity Icon -->
              <div
                :class="[
                  'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center',
                  activity.type === 'document' ? 'bg-blue-100 dark:bg-blue-900/50' :
                  activity.type === 'chat' ? 'bg-green-100 dark:bg-green-900/50' :
                  activity.type === 'template' ? 'bg-purple-100 dark:bg-purple-900/50' : 'bg-gray-100 dark:bg-gray-700'
                ]"
              >
                <svg
                  :class="[
                    'w-5 h-5',
                    activity.type === 'document' ? 'text-blue-600 dark:text-blue-400' :
                    activity.type === 'chat' ? 'text-green-600 dark:text-green-400' :
                    activity.type === 'template' ? 'text-purple-600 dark:text-purple-400' : 'text-gray-500 dark:text-gray-400'
                  ]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    v-if="activity.type === 'document'"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                  <path
                    v-else-if="activity.type === 'chat'"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                  />
                  <path
                    v-else-if="activity.type === 'template'"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                  />
                </svg>
              </div>

              <!-- Activity Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-sm font-medium text-gray-900 dark:text-white">
                      {{ activity.title }}
                    </h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {{ activity.description }}
                    </p>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span
                      :class="[
                        'px-2 py-1 text-xs font-medium rounded-full',
                        activity.status === 'completed' ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200' :
                        activity.status === 'processing' ? 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-200' :
                        activity.status === 'failed' ? 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200' :
                        'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                      ]"
                    >
                      {{ activity.status }}
                    </span>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      {{ formatDate(activity.createdAt) }}
                    </div>
                  </div>
                </div>

                <!-- Activity Details -->
                <div v-if="activity.details" class="mt-3 text-xs text-gray-500 dark:text-gray-400">
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div v-if="activity.details.fileSize">
                      <span class="font-medium">File Size:</span> {{ formatFileSize(activity.details.fileSize) }}
                    </div>
                    <div v-if="activity.details.tokensUsed">
                      <span class="font-medium">Tokens:</span> {{ activity.details.tokensUsed.toLocaleString() }}
                    </div>
                    <div v-if="activity.details.duration">
                      <span class="font-medium">Duration:</span> {{ activity.details.duration }}
                    </div>
                    <div v-if="activity.details.model">
                      <span class="font-medium">Model:</span> {{ activity.details.model }}
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="mt-3 flex items-center space-x-3">
                  <button
                    v-if="activity.type === 'document' && activity.status === 'completed'"
                    @click="viewDocument(activity)"
                    class="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
                  >
                    View Results
                  </button>
                  <button
                    v-if="activity.type === 'chat'"
                    @click="viewChat(activity)"
                    class="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
                  >
                    View Chat
                  </button>
                  <button
                    v-if="activity.type === 'template' && activity.status === 'completed'"
                    @click="downloadTemplate(activity)"
                    class="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
                  >
                    Download
                  </button>
                  <button
                    @click="deleteActivity(activity)"
                    class="text-xs text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 font-medium"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="filteredActivities.length > itemsPerPage" class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-700 dark:text-gray-300">
              Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredActivities.length) }} 
              of {{ filteredActivities.length }} results
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span class="px-3 py-1 text-sm">
                Page {{ currentPage }} of {{ totalPages }}
              </span>
              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useAppStore } from '../store'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

// Reactive data
const loading = ref(false)
const selectedFilter = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10

const dateRange = reactive({
  start: '',
  end: ''
})

const totalStats = reactive({
  documents: 42,
  chats: 156,
  templates: 38,
  tokensUsed: 75000
})

// Mock activities data (replace with real API calls)
const activities = reactive([
  {
    id: 1,
    type: 'document',
    title: 'Advanced Programming Concepts.pdf',
    description: 'Uploaded and processed curriculum document',
    status: 'completed',
    createdAt: '2024-06-05T10:00:00Z',
    details: {
      fileSize: 2048576,
      tokensUsed: 1500,
      duration: '2m 34s'
    }
  },
  {
    id: 2,
    type: 'chat',
    title: 'Software Engineering Standards Discussion',
    description: 'AI chat session about NOSS development',
    status: 'completed',
    createdAt: '2024-06-05T08:00:00Z',
    details: {
      tokensUsed: 800,
      duration: '15m 20s',
      model: 'GPT-4'
    }
  },
  {
    id: 3,
    type: 'template',
    title: 'Database Management NOSS Template',
    description: 'Generated comprehensive NOSS template',
    status: 'completed',
    createdAt: '2024-06-04T15:30:00Z',
    details: {
      tokensUsed: 2200,
      duration: '3m 45s',
      model: 'Claude-3'
    }
  },
  {
    id: 4,
    type: 'document',
    title: 'Skills Assessment Framework.docx',
    description: 'Processing skills assessment document',
    status: 'processing',
    createdAt: '2024-06-04T14:20:00Z',
    details: {
      fileSize: 1024000
    }
  },
  {
    id: 5,
    type: 'chat',
    title: 'Learning Objectives Analysis',
    description: 'AI analysis of curriculum learning objectives',
    status: 'completed',
    createdAt: '2024-06-03T11:45:00Z',
    details: {
      tokensUsed: 1200,
      duration: '8m 12s',
      model: 'GPT-4'
    }
  }
])

// Computed properties
const filteredActivities = computed(() => {
  let filtered = activities

  // Filter by type
  if (selectedFilter.value !== 'all') {
    const filterType = selectedFilter.value === 'chats' ? 'chat' : selectedFilter.value.slice(0, -1)
    filtered = filtered.filter(activity => activity.type === filterType)
  }

  // Filter by date range
  if (dateRange.start && dateRange.end) {
    filtered = filtered.filter(activity => {
      const activityDate = new Date(activity.createdAt).toISOString().split('T')[0]
      return activityDate >= dateRange.start && activityDate <= dateRange.end
    })
  }

  return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const paginatedActivities = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredActivities.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredActivities.value.length / itemsPerPage)
})

// Methods
const applyFilter = () => {
  currentPage.value = 1
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatFileSize = (bytes) => {
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  if (bytes === 0) return '0 Bytes'
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

const viewDocument = (activity) => {
  // Navigate to document view or open in new tab
  router.push(`/documents/${activity.id}`)
}

const viewChat = (activity) => {
  // Navigate to chat history
  router.push(`/chat/${activity.id}`)
}

const downloadTemplate = (activity) => {
  // Download template file
  appStore.addNotification({
    type: 'info',
    title: 'Download started',
    message: `Downloading ${activity.title}`
  })
  // TODO: Implement actual download logic
}

const deleteActivity = async (activity) => {
  if (confirm(`Are you sure you want to delete "${activity.title}"?`)) {
    try {
      // TODO: Implement actual delete API call
      const index = activities.findIndex(a => a.id === activity.id)
      if (index > -1) {
        activities.splice(index, 1)
      }
      
      appStore.addNotification({
        type: 'success',
        title: 'Activity deleted',
        message: `"${activity.title}" has been deleted`
      })
    } catch (error) {
      appStore.addNotification({
        type: 'error',
        title: 'Delete failed',
        message: error.message || 'Failed to delete activity'
      })
    }
  }
}

// Load history data
onMounted(async () => {
  try {
    loading.value = true
    // TODO: Replace with actual API calls
    // const response = await fetch('/api/history')
    // const data = await response.json()
    // activities.splice(0, activities.length, ...data.activities)
    // Object.assign(totalStats, data.stats)
  } catch (error) {
    appStore.addNotification({
      type: 'error',
      title: 'Failed to load history',
      message: error.message || 'Unable to load activity history'
    })
  } finally {
    loading.value = false
  }
})
</script>
