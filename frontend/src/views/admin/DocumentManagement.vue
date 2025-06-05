<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Document Management</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              Manage uploaded documents and processed files
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="bulkActions = !bulkActions"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              Bulk Actions
            </button>
            <button
              @click="showUploadModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Upload Document
            </button>
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div
          v-for="stat in documentStats"
          :key="stat.id"
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg"
        >
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div :class="['w-8 h-8 rounded-md flex items-center justify-center', stat.bgColor]">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="stat.icon"></svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">{{ stat.label }}</dt>
                  <dd class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stat.value }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg mb-6">
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- Search -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Search Documents
              </label>
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search by filename, type, or user..."
                  class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            </div>

            <!-- Status Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Status
              </label>
              <select
                v-model="selectedStatus"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Status</option>
                <option value="processed">Processed</option>
                <option value="processing">Processing</option>
                <option value="failed">Failed</option>
                <option value="queued">Queued</option>
              </select>
            </div>

            <!-- File Type Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                File Type
              </label>
              <select
                v-model="selectedFileType"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="pdf">PDF</option>
                <option value="docx">Word Document</option>
                <option value="xlsx">Excel</option>
                <option value="txt">Text</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Bulk Actions Bar -->
      <div v-if="bulkActions && selectedDocuments.length > 0" class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-sm font-medium text-blue-900 dark:text-blue-100">
              {{ selectedDocuments.length }} document(s) selected
            </span>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="bulkReprocess"
              class="inline-flex items-center px-3 py-2 border border-blue-300 dark:border-blue-600 shadow-sm text-sm leading-4 font-medium rounded-md text-blue-700 dark:text-blue-300 bg-white dark:bg-gray-800 hover:bg-blue-50 dark:hover:bg-blue-900/50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Reprocess
            </button>
            <button
              @click="bulkDownload"
              class="inline-flex items-center px-3 py-2 border border-blue-300 dark:border-blue-600 shadow-sm text-sm leading-4 font-medium rounded-md text-blue-700 dark:text-blue-300 bg-white dark:bg-gray-800 hover:bg-blue-50 dark:hover:bg-blue-900/50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download
            </button>
            <button
              @click="bulkDelete"
              class="inline-flex items-center px-3 py-2 border border-red-300 dark:border-red-600 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 dark:text-red-300 bg-white dark:bg-gray-800 hover:bg-red-50 dark:hover:bg-red-900/50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Delete
            </button>
            <button
              @click="clearSelection"
              class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
            >
              Clear Selection
            </button>
          </div>
        </div>
      </div>

      <!-- Documents Table -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th v-if="bulkActions" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  <input
                    type="checkbox"
                    :checked="selectedDocuments.length === filteredDocuments.length && filteredDocuments.length > 0"
                    @change="toggleSelectAll"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
                  >
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Document
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Size
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Uploaded By
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Date
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr
                v-for="document in paginatedDocuments"
                :key="document.id"
                :class="{ 'bg-blue-50 dark:bg-blue-900/20': selectedDocuments.includes(document.id) }"
              >
                <td v-if="bulkActions" class="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    :checked="selectedDocuments.includes(document.id)"
                    @change="toggleDocumentSelection(document.id)"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded"
                  >
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div :class="[
                        'h-10 w-10 rounded-lg flex items-center justify-center',
                        getFileTypeColor(document.type)
                      ]">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="getFileTypeIcon(document.type)"></svg>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">{{ document.filename }}</div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">{{ document.type.toUpperCase() }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    getStatusColor(document.status)
                  ]">
                    <svg :class="[
                      'w-1.5 h-1.5 mr-1.5',
                      document.status === 'processing' ? 'animate-pulse' : ''
                    ]" fill="currentColor" viewBox="0 0 8 8">
                      <circle cx="4" cy="4" r="3" />
                    </svg>
                    {{ document.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatFileSize(document.size) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900 dark:text-white">{{ document.uploadedBy }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ document.userRole }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(document.uploadedAt) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <button
                      @click="viewDocument(document)"
                      class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                    >
                      View
                    </button>
                    <button
                      @click="downloadDocument(document)"
                      class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
                    >
                      Download
                    </button>
                    <button
                      v-if="document.status === 'failed'"
                      @click="reprocessDocument(document)"
                      class="text-yellow-600 dark:text-yellow-400 hover:text-yellow-900 dark:hover:text-yellow-300"
                    >
                      Reprocess
                    </button>
                    <button
                      @click="deleteDocument(document)"
                      class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="bg-white dark:bg-gray-800 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="previousPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700 dark:text-gray-300">
                Showing
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                to
                <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, filteredDocuments.length) }}</span>
                of
                <span class="font-medium">{{ filteredDocuments.length }}</span>
                results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button
                  @click="previousPage"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="goToPage(page)"
                  :class="[
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                    page === currentPage
                      ? 'z-10 bg-blue-50 dark:bg-blue-900/50 border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700'
                  ]"
                >
                  {{ page }}
                </button>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showUploadModal = false">
      <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-md shadow-lg rounded-md bg-white dark:bg-gray-800" @click.stop>
        <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Upload Document</h3>
          <button @click="showUploadModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-4">
          <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <div class="mt-4">
              <label for="file-upload" class="cursor-pointer">
                <span class="mt-2 block text-sm font-medium text-gray-900 dark:text-white">
                  Drop files here or click to browse
                </span>
                <input id="file-upload" name="file-upload" type="file" class="sr-only" multiple accept=".pdf,.docx,.xlsx,.txt">
              </label>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                PDF, DOCX, XLSX, TXT up to 10MB
              </p>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button
              @click="showUploadModal = false"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
            <button
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Upload
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useAppStore } from '../../store'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

// Reactive data
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedFileType = ref('')
const bulkActions = ref(false)
const selectedDocuments = ref([])
const showUploadModal = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Document statistics
const documentStats = reactive([
  {
    id: 1,
    label: 'Total Documents',
    value: '2,847',
    bgColor: 'bg-blue-500',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />'
  },
  {
    id: 2,
    label: 'Processed',
    value: '2,543',
    bgColor: 'bg-green-500',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />'
  },
  {
    id: 3,
    label: 'Processing',
    value: '23',
    bgColor: 'bg-yellow-500',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />'
  },
  {
    id: 4,
    label: 'Failed',
    value: '47',
    bgColor: 'bg-red-500',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />'
  }
])

// Mock documents data
const documents = reactive([
  {
    id: 1,
    filename: 'NOSS_Software_Development.pdf',
    type: 'pdf',
    status: 'processed',
    size: 2456789,
    uploadedBy: 'John Doe',
    userRole: 'Administrator',
    uploadedAt: '2024-01-15T10:30:00Z',
    processedAt: '2024-01-15T10:32:15Z'
  },
  {
    id: 2,
    filename: 'Healthcare_Competencies.docx',
    type: 'docx',
    status: 'processing',
    size: 987654,
    uploadedBy: 'Jane Smith',
    userRole: 'Content Manager',
    uploadedAt: '2024-01-15T11:15:00Z',
    processedAt: null
  },
  {
    id: 3,
    filename: 'Assessment_Criteria.xlsx',
    type: 'xlsx',
    status: 'failed',
    size: 1234567,
    uploadedBy: 'Mike Johnson',
    userRole: 'Educator',
    uploadedAt: '2024-01-15T09:45:00Z',
    processedAt: null
  },
  {
    id: 4,
    filename: 'Training_Manual.pdf',
    type: 'pdf',
    status: 'processed',
    size: 3456789,
    uploadedBy: 'Sarah Wilson',
    userRole: 'Administrator',
    uploadedAt: '2024-01-14T16:20:00Z',
    processedAt: '2024-01-14T16:25:30Z'
  },
  {
    id: 5,
    filename: 'Learning_Outcomes.txt',
    type: 'txt',
    status: 'queued',
    size: 45678,
    uploadedBy: 'David Brown',
    userRole: 'Content Manager',
    uploadedAt: '2024-01-15T12:00:00Z',
    processedAt: null
  }
])

// Computed properties
const filteredDocuments = computed(() => {
  return documents.filter(doc => {
    const matchesSearch = !searchQuery.value || 
      doc.filename.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.uploadedBy.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.type.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesStatus = !selectedStatus.value || doc.status === selectedStatus.value
    const matchesFileType = !selectedFileType.value || doc.type === selectedFileType.value
    
    return matchesSearch && matchesStatus && matchesFileType
  })
})

const paginatedDocuments = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredDocuments.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredDocuments.value.length / itemsPerPage.value)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const getFileTypeIcon = (type) => {
  const icons = {
    pdf: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />',
    docx: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />',
    xlsx: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />',
    txt: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />'
  }
  return icons[type] || icons.txt
}

const getFileTypeColor = (type) => {
  const colors = {
    pdf: 'bg-red-500',
    docx: 'bg-blue-500',
    xlsx: 'bg-green-500',
    txt: 'bg-gray-500'
  }
  return colors[type] || colors.txt
}

const getStatusColor = (status) => {
  const colors = {
    processed: 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-200',
    processing: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-200',
    failed: 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200',
    queued: 'bg-gray-100 text-gray-800 dark:bg-gray-900/50 dark:text-gray-200'
  }
  return colors[status] || colors.queued
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const toggleSelectAll = () => {
  if (selectedDocuments.value.length === filteredDocuments.value.length) {
    selectedDocuments.value = []
  } else {
    selectedDocuments.value = filteredDocuments.value.map(doc => doc.id)
  }
}

const toggleDocumentSelection = (docId) => {
  const index = selectedDocuments.value.indexOf(docId)
  if (index > -1) {
    selectedDocuments.value.splice(index, 1)
  } else {
    selectedDocuments.value.push(docId)
  }
}

const clearSelection = () => {
  selectedDocuments.value = []
}

const viewDocument = (document) => {
  // TODO: Implement document viewer
  appStore.addNotification({
    type: 'info',
    title: 'Document Viewer',
    message: `Opening ${document.filename}`
  })
}

const downloadDocument = (document) => {
  // TODO: Implement document download
  appStore.addNotification({
    type: 'success',
    title: 'Download Started',
    message: `Downloading ${document.filename}`
  })
}

const reprocessDocument = async (document) => {
  try {
    // TODO: Implement document reprocessing
    document.status = 'processing'
    
    // Simulate processing
    setTimeout(() => {
      document.status = 'processed'
      document.processedAt = new Date().toISOString()
    }, 3000)
    
    appStore.addNotification({
      type: 'info',
      title: 'Reprocessing Started',
      message: `Reprocessing ${document.filename}`
    })
  } catch (error) {
    appStore.addNotification({
      type: 'error',
      title: 'Reprocess Failed',
      message: `Failed to reprocess ${document.filename}`
    })
  }
}

const deleteDocument = async (document) => {
  if (confirm(`Are you sure you want to delete "${document.filename}"?`)) {
    try {
      // TODO: Implement document deletion
      const index = documents.findIndex(doc => doc.id === document.id)
      if (index > -1) {
        documents.splice(index, 1)
      }
      
      appStore.addNotification({
        type: 'success',
        title: 'Document Deleted',
        message: `${document.filename} has been deleted`
      })
    } catch (error) {
      appStore.addNotification({
        type: 'error',
        title: 'Delete Failed',
        message: `Failed to delete ${document.filename}`
      })
    }
  }
}

const bulkReprocess = async () => {
  if (confirm(`Reprocess ${selectedDocuments.value.length} selected documents?`)) {
    try {
      // TODO: Implement bulk reprocessing
      selectedDocuments.value.forEach(docId => {
        const document = documents.find(doc => doc.id === docId)
        if (document && document.status === 'failed') {
          document.status = 'processing'
        }
      })
      
      appStore.addNotification({
        type: 'success',
        title: 'Bulk Reprocess Started',
        message: `Reprocessing ${selectedDocuments.value.length} documents`
      })
      
      clearSelection()
    } catch (error) {
      appStore.addNotification({
        type: 'error',
        title: 'Bulk Reprocess Failed',
        message: 'Failed to start bulk reprocessing'
      })
    }
  }
}

const bulkDownload = async () => {
  try {
    // TODO: Implement bulk download
    appStore.addNotification({
      type: 'success',
      title: 'Bulk Download Started',
      message: `Preparing download for ${selectedDocuments.value.length} documents`
    })
    
    clearSelection()
  } catch (error) {
    appStore.addNotification({
      type: 'error',
      title: 'Bulk Download Failed',
      message: 'Failed to prepare bulk download'
    })
  }
}

const bulkDelete = async () => {
  if (confirm(`Are you sure you want to delete ${selectedDocuments.value.length} selected documents? This action cannot be undone.`)) {
    try {
      // TODO: Implement bulk deletion
      selectedDocuments.value.forEach(docId => {
        const index = documents.findIndex(doc => doc.id === docId)
        if (index > -1) {
          documents.splice(index, 1)
        }
      })
      
      appStore.addNotification({
        type: 'success',
        title: 'Bulk Delete Completed',
        message: `Deleted ${selectedDocuments.value.length} documents`
      })
      
      clearSelection()
    } catch (error) {
      appStore.addNotification({
        type: 'error',
        title: 'Bulk Delete Failed',
        message: 'Failed to delete selected documents'
      })
    }
  }
}

// Pagination methods
const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page) => {
  currentPage.value = page
}

// Initialize
onMounted(() => {
  // TODO: Load documents from API
})
</script>

<style scoped>
/* Custom scrollbar */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400 dark:bg-gray-500;
}

/* Animation for processing status */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
