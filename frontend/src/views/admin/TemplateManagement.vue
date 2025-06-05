<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Template Management</h1>
        <p class="text-gray-600 dark:text-gray-400">Manage NOSS templates and generation settings</p>
      </div>
      <div class="flex space-x-3">
        <button @click="showCreateModal = true" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Create Template
        </button>
        <button @click="showImportModal = true" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
          </svg>
          Import Template
        </button>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Templates</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ templateStats.total }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 dark:bg-green-900">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Templates</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ templateStats.active }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Usage This Month</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ templateStats.monthlyUsage }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100 dark:bg-orange-900">
            <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Review</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ templateStats.pendingReview }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <div class="relative">
            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search templates..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
          </div>
        </div>
        <div class="flex gap-4">
          <select v-model="selectedType" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white">
            <option value="">All Types</option>
            <option value="competency">Competency Units</option>
            <option value="assessment">Assessment Guidelines</option>
            <option value="curriculum">Full Curriculum</option>
            <option value="lesson">Lesson Plans</option>
          </select>
          <select v-model="selectedStatus" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="draft">Draft</option>
            <option value="archived">Archived</option>
            <option value="pending">Pending Review</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Templates Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Templates</h3>
          <div class="flex items-center space-x-2">
            <button @click="selectAll" class="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400">
              {{ selectedTemplates.length === filteredTemplates.length ? 'Deselect All' : 'Select All' }}
            </button>
            <span class="text-gray-300 dark:text-gray-600">|</span>
            <div class="flex space-x-2">
              <button 
                @click="bulkActivate"
                :disabled="selectedTemplates.length === 0"
                class="text-sm text-green-600 hover:text-green-800 dark:text-green-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Activate Selected
              </button>
              <button 
                @click="bulkArchive"
                :disabled="selectedTemplates.length === 0"
                class="text-sm text-orange-600 hover:text-orange-800 dark:text-orange-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Archive Selected
              </button>
              <button 
                @click="bulkDelete"
                :disabled="selectedTemplates.length === 0"
                class="text-sm text-red-600 hover:text-red-800 dark:text-red-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Delete Selected
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                <input type="checkbox" @change="toggleSelectAll" class="rounded border-gray-300 dark:border-gray-600">
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Template</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Usage</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Created</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="template in paginatedTemplates" :key="template.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap">
                <input 
                  type="checkbox" 
                  :value="template.id"
                  v-model="selectedTemplates"
                  class="rounded border-gray-300 dark:border-gray-600"
                >
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                      <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ template.name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ template.description }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getTypeClass(template.type)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ template.type }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusClass(template.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ template.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ template.usageCount }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ formatDate(template.createdAt) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button @click="editTemplate(template)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button @click="duplicateTemplate(template)" class="text-green-600 hover:text-green-900 dark:text-green-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                  <button @click="deleteTemplate(template)" class="text-red-600 hover:text-red-900 dark:text-red-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="bg-white dark:bg-gray-800 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700 dark:text-gray-300">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredTemplates.length) }} of {{ filteredTemplates.length }} templates
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span class="text-sm text-gray-700 dark:text-gray-300">
              Page {{ currentPage }} of {{ totalPages }}
            </span>
            <button
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Template Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ showEditModal ? 'Edit Template' : 'Create New Template' }}
          </h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveTemplate" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Template Name</label>
            <input
              v-model="templateForm.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
            <textarea
              v-model="templateForm.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Template Type</label>
            <select
              v-model="templateForm.type"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="">Select type...</option>
              <option value="competency">Competency Units</option>
              <option value="assessment">Assessment Guidelines</option>
              <option value="curriculum">Full Curriculum</option>
              <option value="lesson">Lesson Plans</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Template Content</label>
            <textarea
              v-model="templateForm.content"
              rows="10"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white font-mono text-sm"
              placeholder="Enter template content with variables like {{title}}, {{industry}}, {{skillLevel}}, etc."
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
            <select
              v-model="templateForm.status"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="draft">Draft</option>
              <option value="active">Active</option>
              <option value="pending">Pending Review</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              {{ showEditModal ? 'Update Template' : 'Create Template' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Import Template Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-lg">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Import Template</h3>
          <button @click="showImportModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="space-y-6">
          <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3-3m-3 3l3 3m3-3H21m-8-8v8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <div class="mt-4">
              <label class="cursor-pointer">
                <span class="mt-2 block text-sm font-medium text-gray-900 dark:text-white">
                  Drop template file here or click to browse
                </span>
                <input type="file" class="hidden" accept=".json,.xml,.docx" @change="handleFileUpload">
              </label>
            </div>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Supports JSON, XML, and DOCX files
            </p>
          </div>

          <div class="flex justify-end space-x-4">
            <button
              @click="showImportModal = false"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500"
            >
              Cancel
            </button>
            <button
              :disabled="!importFile"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Import Template
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'TemplateManagement',
  setup() {
    // Reactive data
    const templates = ref([])
    const selectedTemplates = ref([])
    const searchQuery = ref('')
    const selectedType = ref('')
    const selectedStatus = ref('')
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    
    // Modals
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const showImportModal = ref(false)
    const importFile = ref(null)
    
    // Form data
    const templateForm = ref({
      id: null,
      name: '',
      description: '',
      type: '',
      content: '',
      status: 'draft'
    })

    // Template statistics
    const templateStats = ref({
      total: 156,
      active: 134,
      monthlyUsage: 2847,
      pendingReview: 8
    })

    // Computed properties
    const filteredTemplates = computed(() => {
      return templates.value.filter(template => {
        const matchesSearch = !searchQuery.value || 
          template.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          template.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        
        const matchesType = !selectedType.value || template.type === selectedType.value
        const matchesStatus = !selectedStatus.value || template.status === selectedStatus.value
        
        return matchesSearch && matchesType && matchesStatus
      })
    })

    const paginatedTemplates = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredTemplates.value.slice(start, end)
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredTemplates.value.length / itemsPerPage.value)
    })

    // Methods
    const loadTemplates = () => {
      // TODO: Replace with actual API call
      templates.value = [
        {
          id: 1,
          name: 'Basic Competency Unit Template',
          description: 'Standard template for creating competency units',
          type: 'competency',
          status: 'active',
          usageCount: 245,
          createdAt: '2024-01-15T10:30:00Z',
          content: 'Template content here...'
        },
        {
          id: 2,
          name: 'Assessment Guidelines Template',
          description: 'Template for assessment criteria and guidelines',
          type: 'assessment',
          status: 'active',
          usageCount: 189,
          createdAt: '2024-01-20T14:45:00Z',
          content: 'Assessment template content...'
        },
        {
          id: 3,
          name: 'Full Curriculum Template',
          description: 'Comprehensive curriculum development template',
          type: 'curriculum',
          status: 'active',
          usageCount: 67,
          createdAt: '2024-02-01T09:15:00Z',
          content: 'Curriculum template content...'
        },
        {
          id: 4,
          name: 'Lesson Plan Template',
          description: 'Template for creating detailed lesson plans',
          type: 'lesson',
          status: 'pending',
          usageCount: 34,
          createdAt: '2024-02-10T16:20:00Z',
          content: 'Lesson plan template content...'
        },
        {
          id: 5,
          name: 'Advanced Assessment Template',
          description: 'Advanced template for complex assessments',
          type: 'assessment',
          status: 'draft',
          usageCount: 0,
          createdAt: '2024-02-15T11:00:00Z',
          content: 'Advanced assessment template...'
        }
      ]
    }

    const getTypeClass = (type) => {
      const classes = {
        competency: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
        assessment: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
        curriculum: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
        lesson: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
      }
      return classes[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }

    const getStatusClass = (status) => {
      const classes = {
        active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
        draft: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300',
        pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
        archived: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
      }
      return classes[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const selectAll = () => {
      if (selectedTemplates.value.length === filteredTemplates.value.length) {
        selectedTemplates.value = []
      } else {
        selectedTemplates.value = filteredTemplates.value.map(t => t.id)
      }
    }

    const toggleSelectAll = (event) => {
      if (event.target.checked) {
        selectedTemplates.value = filteredTemplates.value.map(t => t.id)
      } else {
        selectedTemplates.value = []
      }
    }

    const bulkActivate = () => {
      // TODO: Implement bulk activate
      console.log('Bulk activate:', selectedTemplates.value)
      selectedTemplates.value = []
    }

    const bulkArchive = () => {
      // TODO: Implement bulk archive
      console.log('Bulk archive:', selectedTemplates.value)
      selectedTemplates.value = []
    }

    const bulkDelete = () => {
      if (confirm('Are you sure you want to delete the selected templates?')) {
        // TODO: Implement bulk delete
        console.log('Bulk delete:', selectedTemplates.value)
        selectedTemplates.value = []
      }
    }

    const editTemplate = (template) => {
      templateForm.value = { ...template }
      showEditModal.value = true
    }

    const duplicateTemplate = (template) => {
      const newTemplate = {
        ...template,
        id: Date.now(),
        name: `${template.name} (Copy)`,
        status: 'draft',
        usageCount: 0,
        createdAt: new Date().toISOString()
      }
      templates.value.push(newTemplate)
    }

    const deleteTemplate = (template) => {
      if (confirm(`Are you sure you want to delete "${template.name}"?`)) {
        const index = templates.value.findIndex(t => t.id === template.id)
        if (index > -1) {
          templates.value.splice(index, 1)
        }
      }
    }

    const saveTemplate = () => {
      if (showEditModal.value) {
        // Update existing template
        const index = templates.value.findIndex(t => t.id === templateForm.value.id)
        if (index > -1) {
          templates.value[index] = { ...templateForm.value }
        }
      } else {
        // Create new template
        const newTemplate = {
          ...templateForm.value,
          id: Date.now(),
          usageCount: 0,
          createdAt: new Date().toISOString()
        }
        templates.value.push(newTemplate)
      }
      closeModal()
    }

    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      templateForm.value = {
        id: null,
        name: '',
        description: '',
        type: '',
        content: '',
        status: 'draft'
      }
    }

    const handleFileUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        importFile.value = file
        // TODO: Process the uploaded file
        console.log('File uploaded:', file.name)
      }
    }

    // Lifecycle
    onMounted(() => {
      loadTemplates()
    })

    return {
      // Data
      templates,
      selectedTemplates,
      searchQuery,
      selectedType,
      selectedStatus,
      currentPage,
      itemsPerPage,
      templateStats,
      
      // Modals
      showCreateModal,
      showEditModal,
      showImportModal,
      importFile,
      
      // Form
      templateForm,
      
      // Computed
      filteredTemplates,
      paginatedTemplates,
      totalPages,
      
      // Methods
      getTypeClass,
      getStatusClass,
      formatDate,
      selectAll,
      toggleSelectAll,
      bulkActivate,
      bulkArchive,
      bulkDelete,
      editTemplate,
      duplicateTemplate,
      deleteTemplate,
      saveTemplate,
      closeModal,
      handleFileUpload
    }
  }
}
</script>
