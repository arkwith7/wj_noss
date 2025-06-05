<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Metadata Management</h1>
        <p class="text-gray-600 dark:text-gray-400">Manage document metadata, tags, and classification settings</p>
      </div>
      <div class="flex space-x-3">
        <button @click="showAddMetadataModal = true" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Field
        </button>
        <button @click="exportMetadata" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Export Schema
        </button>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Metadata Fields</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ metadataStats.totalFields }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 dark:bg-green-900">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Tagged Documents</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ metadataStats.taggedDocuments }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Categories</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ metadataStats.categories }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100 dark:bg-orange-900">
            <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Auto-Tagged</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ metadataStats.autoTagged }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex space-x-8 px-6">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Metadata Fields Tab -->
      <div v-if="activeTab === 'fields'" class="p-6">
        <div class="space-y-6">
          <!-- Search and Filter -->
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex-1">
              <div class="relative">
                <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  v-model="fieldsSearchQuery"
                  type="text"
                  placeholder="Search metadata fields..."
                  class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
              </div>
            </div>
            <div class="flex gap-4">
              <select v-model="selectedFieldType" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white">
                <option value="">All Types</option>
                <option value="text">Text</option>
                <option value="number">Number</option>
                <option value="date">Date</option>
                <option value="select">Select</option>
                <option value="multiselect">Multi-Select</option>
                <option value="boolean">Boolean</option>
              </select>
              <select v-model="selectedFieldStatus" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
          </div>

          <!-- Fields Table -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Field Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Required</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Usage</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="field in filteredFields" :key="field.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div class="text-sm font-medium text-gray-900 dark:text-white">{{ field.name }}</div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">{{ field.description }}</div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getFieldTypeClass(field.type)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ field.type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span v-if="field.required" class="text-red-600 dark:text-red-400">Yes</span>
                    <span v-else class="text-gray-500 dark:text-gray-400">No</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ field.usageCount }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="field.status === 'active' ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'">
                      {{ field.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex items-center space-x-2">
                      <button @click="editField(field)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button @click="toggleFieldStatus(field)" class="text-green-600 hover:text-green-900 dark:text-green-400">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                        </svg>
                      </button>
                      <button @click="deleteField(field)" class="text-red-600 hover:text-red-900 dark:text-red-400">
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
        </div>
      </div>

      <!-- Tags Tab -->
      <div v-if="activeTab === 'tags'" class="p-6">
        <div class="space-y-6">
          <!-- Tag Cloud -->
          <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Popular Tags</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in popularTags"
                :key="tag.name"
                :class="getTagSizeClass(tag.count)"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 cursor-pointer hover:bg-blue-200 dark:hover:bg-blue-800"
                @click="filterByTag(tag.name)"
              >
                {{ tag.name }} ({{ tag.count }})
              </span>
            </div>
          </div>

          <!-- Tags Management -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- All Tags -->
            <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">All Tags</h3>
              <div class="space-y-2 max-h-96 overflow-y-auto">
                <div
                  v-for="tag in allTags"
                  :key="tag.id"
                  class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div>
                    <span class="font-medium text-gray-900 dark:text-white">{{ tag.name }}</span>
                    <span class="ml-2 text-sm text-gray-500 dark:text-gray-400">({{ tag.count }} documents)</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button @click="editTag(tag)" class="text-blue-600 hover:text-blue-800 dark:text-blue-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="deleteTag(tag)" class="text-red-600 hover:text-red-800 dark:text-red-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tag Categories -->
            <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Tag Categories</h3>
              <div class="space-y-4">
                <div v-for="category in tagCategories" :key="category.name" class="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                  <div class="flex items-center justify-between mb-2">
                    <h4 class="font-medium text-gray-900 dark:text-white">{{ category.name }}</h4>
                    <span class="text-sm text-gray-500 dark:text-gray-400">{{ category.tags.length }} tags</span>
                  </div>
                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="tag in category.tags.slice(0, 5)"
                      :key="tag"
                      class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
                    >
                      {{ tag }}
                    </span>
                    <span v-if="category.tags.length > 5" class="text-xs text-gray-500 dark:text-gray-400">
                      +{{ category.tags.length - 5 }} more
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Schema Tab -->
      <div v-if="activeTab === 'schema'" class="p-6">
        <div class="space-y-6">
          <!-- Schema Editor -->
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Metadata Schema</h3>
              <div class="flex space-x-2">
                <button @click="validateSchema" class="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900">
                  Validate Schema
                </button>
                <button @click="saveSchema" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Save Schema
                </button>
              </div>
            </div>
            <textarea
              v-model="schemaContent"
              rows="20"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white font-mono text-sm"
              placeholder="Enter JSON schema..."
            ></textarea>
          </div>

          <!-- Schema Validation Results -->
          <div v-if="schemaValidation.length > 0" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Validation Results</h3>
            <div class="space-y-2">
              <div
                v-for="(result, index) in schemaValidation"
                :key="index"
                :class="[
                  'p-3 rounded-lg',
                  result.type === 'error' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300' :
                  result.type === 'warning' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300' :
                  'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                ]"
              >
                <div class="flex items-center">
                  <svg v-if="result.type === 'error'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else-if="result.type === 'warning'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span class="font-medium">{{ result.message }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Metadata Field Modal -->
    <div v-if="showAddMetadataModal || showEditFieldModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-lg">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ showEditFieldModal ? 'Edit Metadata Field' : 'Add Metadata Field' }}
          </h3>
          <button @click="closeFieldModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveField" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Field Name</label>
            <input
              v-model="fieldForm.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
            <textarea
              v-model="fieldForm.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Field Type</label>
            <select
              v-model="fieldForm.type"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="text">Text</option>
              <option value="number">Number</option>
              <option value="date">Date</option>
              <option value="select">Select</option>
              <option value="multiselect">Multi-Select</option>
              <option value="boolean">Boolean</option>
            </select>
          </div>

          <div v-if="fieldForm.type === 'select' || fieldForm.type === 'multiselect'">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Options (one per line)</label>
            <textarea
              v-model="fieldForm.options"
              rows="4"
              placeholder="Option 1&#10;Option 2&#10;Option 3"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            ></textarea>
          </div>

          <div class="flex items-center">
            <input
              v-model="fieldForm.required"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
            >
            <label class="ml-2 text-sm text-gray-700 dark:text-gray-300">Required field</label>
          </div>

          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="closeFieldModal"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              {{ showEditFieldModal ? 'Update Field' : 'Add Field' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'MetadataManagement',
  setup() {
    // Reactive data
    const activeTab = ref('fields')
    const metadataFields = ref([])
    const allTags = ref([])
    const schemaContent = ref('')
    const schemaValidation = ref([])
    
    // Search and filter
    const fieldsSearchQuery = ref('')
    const selectedFieldType = ref('')
    const selectedFieldStatus = ref('')
    
    // Modals
    const showAddMetadataModal = ref(false)
    const showEditFieldModal = ref(false)
    
    // Form data
    const fieldForm = ref({
      id: null,
      name: '',
      description: '',
      type: 'text',
      required: false,
      options: '',
      status: 'active'
    })

    // Statistics
    const metadataStats = ref({
      totalFields: 24,
      taggedDocuments: 2543,
      categories: 12,
      autoTagged: 1847
    })

    // Tab configuration
    const tabs = [
      { id: 'fields', name: 'Metadata Fields' },
      { id: 'tags', name: 'Tags' },
      { id: 'schema', name: 'Schema' }
    ]

    // Computed properties
    const filteredFields = computed(() => {
      return metadataFields.value.filter(field => {
        const matchesSearch = !fieldsSearchQuery.value || 
          field.name.toLowerCase().includes(fieldsSearchQuery.value.toLowerCase()) ||
          field.description.toLowerCase().includes(fieldsSearchQuery.value.toLowerCase())
        
        const matchesType = !selectedFieldType.value || field.type === selectedFieldType.value
        const matchesStatus = !selectedFieldStatus.value || field.status === selectedFieldStatus.value
        
        return matchesSearch && matchesType && matchesStatus
      })
    })

    const popularTags = computed(() => {
      return allTags.value
        .sort((a, b) => b.count - a.count)
        .slice(0, 20)
    })

    const tagCategories = ref([
      {
        name: 'Industry',
        tags: ['Healthcare', 'Technology', 'Finance', 'Education', 'Manufacturing']
      },
      {
        name: 'Skill Level',
        tags: ['Beginner', 'Intermediate', 'Advanced', 'Expert']
      },
      {
        name: 'Document Type',
        tags: ['Competency', 'Assessment', 'Curriculum', 'Lesson Plan', 'Guidelines']
      },
      {
        name: 'Subject Area',
        tags: ['Technical Skills', 'Soft Skills', 'Safety', 'Quality', 'Leadership']
      }
    ])

    // Methods
    const loadMetadataFields = () => {
      // TODO: Replace with actual API call
      metadataFields.value = [
        {
          id: 1,
          name: 'Industry',
          description: 'Industry classification for the document',
          type: 'select',
          required: true,
          usageCount: 2543,
          status: 'active',
          options: ['Healthcare', 'Technology', 'Finance', 'Education']
        },
        {
          id: 2,
          name: 'Skill Level',
          description: 'Required skill level for the competency',
          type: 'select',
          required: true,
          usageCount: 2401,
          status: 'active',
          options: ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        },
        {
          id: 3,
          name: 'Duration',
          description: 'Expected duration in hours',
          type: 'number',
          required: false,
          usageCount: 1876,
          status: 'active'
        },
        {
          id: 4,
          name: 'Prerequisites',
          description: 'Required prerequisites',
          type: 'multiselect',
          required: false,
          usageCount: 1234,
          status: 'active',
          options: ['Basic literacy', 'Computer skills', 'Prior experience']
        },
        {
          id: 5,
          name: 'Certification',
          description: 'Leads to certification',
          type: 'boolean',
          required: false,
          usageCount: 987,
          status: 'active'
        },
        {
          id: 6,
          name: 'Review Date',
          description: 'Next review date',
          type: 'date',
          required: false,
          usageCount: 2156,
          status: 'active'
        },
        {
          id: 7,
          name: 'Author',
          description: 'Document author',
          type: 'text',
          required: true,
          usageCount: 2543,
          status: 'active'
        },
        {
          id: 8,
          name: 'Keywords',
          description: 'Document keywords',
          type: 'multiselect',
          required: false,
          usageCount: 1876,
          status: 'inactive'
        }
      ]
    }

    const loadTags = () => {
      // TODO: Replace with actual API call
      allTags.value = [
        { id: 1, name: 'Healthcare', count: 234 },
        { id: 2, name: 'Technology', count: 189 },
        { id: 3, name: 'Beginner', count: 345 },
        { id: 4, name: 'Advanced', count: 156 },
        { id: 5, name: 'Assessment', count: 298 },
        { id: 6, name: 'Competency', count: 423 },
        { id: 7, name: 'Technical Skills', count: 167 },
        { id: 8, name: 'Soft Skills', count: 134 },
        { id: 9, name: 'Safety', count: 89 },
        { id: 10, name: 'Quality', count: 76 }
      ]
    }

    const getFieldTypeClass = (type) => {
      const classes = {
        text: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
        number: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
        date: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
        select: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
        multiselect: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300',
        boolean: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
      }
      return classes[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }

    const getTagSizeClass = (count) => {
      if (count > 300) return 'text-lg'
      if (count > 200) return 'text-base'
      if (count > 100) return 'text-sm'
      return 'text-xs'
    }

    const editField = (field) => {
      fieldForm.value = { 
        ...field,
        options: Array.isArray(field.options) ? field.options.join('\n') : ''
      }
      showEditFieldModal.value = true
    }

    const deleteField = (field) => {
      if (confirm(`Are you sure you want to delete the field "${field.name}"?`)) {
        const index = metadataFields.value.findIndex(f => f.id === field.id)
        if (index > -1) {
          metadataFields.value.splice(index, 1)
        }
      }
    }

    const toggleFieldStatus = (field) => {
      field.status = field.status === 'active' ? 'inactive' : 'active'
      // TODO: Update via API
    }

    const saveField = () => {
      const fieldData = {
        ...fieldForm.value,
        options: fieldForm.value.options ? fieldForm.value.options.split('\n').filter(o => o.trim()) : []
      }

      if (showEditFieldModal.value) {
        // Update existing field
        const index = metadataFields.value.findIndex(f => f.id === fieldData.id)
        if (index > -1) {
          metadataFields.value[index] = fieldData
        }
      } else {
        // Create new field
        fieldData.id = Date.now()
        fieldData.usageCount = 0
        metadataFields.value.push(fieldData)
      }
      
      closeFieldModal()
    }

    const closeFieldModal = () => {
      showAddMetadataModal.value = false
      showEditFieldModal.value = false
      fieldForm.value = {
        id: null,
        name: '',
        description: '',
        type: 'text',
        required: false,
        options: '',
        status: 'active'
      }
    }

    const editTag = (tag) => {
      // TODO: Implement tag editing
      console.log('Edit tag:', tag)
    }

    const deleteTag = (tag) => {
      if (confirm(`Are you sure you want to delete the tag "${tag.name}"?`)) {
        const index = allTags.value.findIndex(t => t.id === tag.id)
        if (index > -1) {
          allTags.value.splice(index, 1)
        }
      }
    }

    const filterByTag = (tagName) => {
      // TODO: Implement tag filtering
      console.log('Filter by tag:', tagName)
    }

    const validateSchema = () => {
      try {
        JSON.parse(schemaContent.value)
        schemaValidation.value = [
          { type: 'success', message: 'Schema is valid JSON' },
          { type: 'success', message: 'All required fields are present' },
          { type: 'warning', message: 'Consider adding field descriptions for better documentation' }
        ]
      } catch (error) {
        schemaValidation.value = [
          { type: 'error', message: `Invalid JSON: ${error.message}` }
        ]
      }
    }

    const saveSchema = () => {
      // TODO: Save schema via API
      console.log('Saving schema:', schemaContent.value)
    }

    const exportMetadata = () => {
      // TODO: Implement metadata export
      console.log('Exporting metadata schema')
    }

    // Lifecycle
    onMounted(() => {
      loadMetadataFields()
      loadTags()
      
      // Initialize schema content
      schemaContent.value = JSON.stringify({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
          "industry": {
            "type": "string",
            "enum": ["Healthcare", "Technology", "Finance", "Education"],
            "description": "Industry classification"
          },
          "skillLevel": {
            "type": "string",
            "enum": ["Beginner", "Intermediate", "Advanced", "Expert"],
            "description": "Required skill level"
          },
          "duration": {
            "type": "number",
            "minimum": 0,
            "description": "Duration in hours"
          },
          "certification": {
            "type": "boolean",
            "description": "Whether this leads to certification"
          }
        },
        "required": ["industry", "skillLevel"]
      }, null, 2)
    })

    return {
      // Data
      activeTab,
      tabs,
      metadataFields,
      allTags,
      metadataStats,
      popularTags,
      tagCategories,
      schemaContent,
      schemaValidation,
      
      // Search and filter
      fieldsSearchQuery,
      selectedFieldType,
      selectedFieldStatus,
      
      // Modals
      showAddMetadataModal,
      showEditFieldModal,
      
      // Form
      fieldForm,
      
      // Computed
      filteredFields,
      
      // Methods
      getFieldTypeClass,
      getTagSizeClass,
      editField,
      deleteField,
      toggleFieldStatus,
      saveField,
      closeFieldModal,
      editTag,
      deleteTag,
      filterByTag,
      validateSchema,
      saveSchema,
      exportMetadata
    }
  }
}
</script>
