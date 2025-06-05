<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Template Generation</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              Create NOSS templates using AI-powered generation tools
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="showTemplateLibrary = true"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              Template Library
            </button>
            <button
              @click="showGenerationHistory = true"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              History
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Template Configuration Panel -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Template Type Selection -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Template Configuration</h2>
            
            <!-- Template Type -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Template Type
              </label>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div
                  v-for="type in templateTypes"
                  :key="type.id"
                  @click="selectedTemplateType = type.id"
                  :class="[
                    'relative border-2 rounded-lg p-4 cursor-pointer transition-all',
                    selectedTemplateType === type.id
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                  ]"
                >
                  <div class="flex items-center">
                    <div class="flex-shrink-0">
                      <div :class="[
                        'w-8 h-8 rounded-lg flex items-center justify-center',
                        selectedTemplateType === type.id
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                      ]">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="type.icon"></svg>
                      </div>
                    </div>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-gray-900 dark:text-white">{{ type.name }}</h3>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ type.description }}</p>
                    </div>
                  </div>
                  <div v-if="selectedTemplateType === type.id" class="absolute top-2 right-2">
                    <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Industry/Field Selection -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Industry/Field
              </label>
              <select
                v-model="selectedIndustry"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select an industry...</option>
                <option v-for="industry in industries" :key="industry.id" :value="industry.id">
                  {{ industry.name }}
                </option>
              </select>
            </div>

            <!-- Skill Level -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Skill Level
              </label>
              <div class="flex space-x-4">
                <label
                  v-for="level in skillLevels"
                  :key="level.id"
                  class="flex items-center"
                >
                  <input
                    type="radio"
                    :value="level.id"
                    v-model="selectedSkillLevel"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600"
                  >
                  <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ level.name }}</span>
                </label>
              </div>
            </div>

            <!-- Custom Requirements -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Specific Requirements (Optional)
              </label>
              <textarea
                v-model="customRequirements"
                rows="4"
                placeholder="Describe any specific competencies, learning outcomes, or requirements for this template..."
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              ></textarea>
            </div>

            <!-- AI Model Selection -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                AI Model
              </label>
              <select
                v-model="selectedAIModel"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="gpt-4">GPT-4 (Most Capable)</option>
                <option value="gpt-3.5">GPT-3.5 (Faster)</option>
                <option value="claude-3">Claude-3 (Alternative)</option>
              </select>
            </div>

            <!-- Generate Button -->
            <div class="flex justify-end">
              <button
                @click="generateTemplate"
                :disabled="!canGenerate || isGenerating"
                class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg v-if="isGenerating" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                {{ isGenerating ? 'Generating...' : 'Generate Template' }}
              </button>
            </div>
          </div>

          <!-- Generation Progress -->
          <div v-if="generationProgress.show" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Generation Progress</h3>
            <div class="space-y-4">
              <div v-for="step in generationProgress.steps" :key="step.id" class="flex items-center">
                <div class="flex-shrink-0">
                  <div v-if="step.status === 'completed'" class="w-8 h-8 bg-green-100 dark:bg-green-900/50 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div v-else-if="step.status === 'processing'" class="w-8 h-8 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </div>
                  <div v-else class="w-8 h-8 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
                    <div class="w-3 h-3 bg-gray-400 dark:bg-gray-500 rounded-full"></div>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ step.name }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ step.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Generated Template Preview -->
          <div v-if="generatedTemplate" class="bg-white dark:bg-gray-800 rounded-lg shadow">
            <div class="p-6 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900 dark:text-white">Generated Template</h3>
                <div class="flex items-center space-x-2">
                  <button
                    @click="editTemplate"
                    class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Edit
                  </button>
                  <button
                    @click="saveTemplate"
                    class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                    </svg>
                    Save
                  </button>
                  <button
                    @click="downloadTemplate"
                    class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Download
                  </button>
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="prose dark:prose-invert max-w-none">
                <div class="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 font-mono bg-gray-50 dark:bg-gray-900 p-4 rounded-lg overflow-auto max-h-96">{{ generatedTemplate.content }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Quick Actions -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h3>
            <div class="space-y-3">
              <button
                v-for="action in quickActions"
                :key="action.id"
                @click="action.action"
                class="w-full flex items-center p-3 text-left border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="action.icon"></svg>
                  </div>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ action.name }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ action.description }}</p>
                </div>
              </button>
            </div>
          </div>

          <!-- Generation Statistics -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Statistics</h3>
            <div class="space-y-4">
              <div v-for="stat in generationStats" :key="stat.id" class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-2 h-2 rounded-full mr-3" :class="stat.color"></div>
                  <span class="text-sm text-gray-600 dark:text-gray-400">{{ stat.label }}</span>
                </div>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ stat.value }}</span>
              </div>
            </div>
          </div>

          <!-- Recent Templates -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent Templates</h3>
            <div class="space-y-3">
              <div
                v-for="template in recentTemplates"
                :key="template.id"
                class="flex items-center p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                @click="loadTemplate(template)"
              >
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-3 flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ template.name }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ template.industry }} • {{ template.createdAt }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Template Library Modal -->
    <div v-if="showTemplateLibrary" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showTemplateLibrary = false">
      <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white dark:bg-gray-800" @click.stop>
        <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Template Library</h3>
          <button @click="showTemplateLibrary = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-4">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="template in templateLibrary"
              :key="template.id"
              class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer"
              @click="useTemplate(template)"
            >
              <h4 class="font-medium text-gray-900 dark:text-white">{{ template.name }}</h4>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ template.description }}</p>
              <div class="flex items-center mt-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200">
                  {{ template.industry }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Generation History Modal -->
    <div v-if="showGenerationHistory" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showGenerationHistory = false">
      <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white dark:bg-gray-800" @click.stop>
        <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Generation History</h3>
          <button @click="showGenerationHistory = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-4">
          <div class="space-y-4">
            <div
              v-for="item in generationHistory"
              :key="item.id"
              class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
            >
              <div class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-white">{{ item.name }}</h4>
                  <p class="text-sm text-gray-500 dark:text-gray-400">{{ item.industry }} • {{ item.type }} • {{ item.createdAt }}</p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  @click="viewTemplate(item)"
                  class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                >
                  View
                </button>
                <button
                  @click="deleteTemplate(item)"
                  class="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
                >
                  Delete
                </button>
              </div>
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
const selectedTemplateType = ref('')
const selectedIndustry = ref('')
const selectedSkillLevel = ref('')
const customRequirements = ref('')
const selectedAIModel = ref('gpt-4')
const isGenerating = ref(false)
const generatedTemplate = ref(null)
const showTemplateLibrary = ref(false)
const showGenerationHistory = ref(false)

// Template types
const templateTypes = [
  {
    id: 'competency',
    name: 'Competency Units',
    description: 'Core skill competencies',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />'
  },
  {
    id: 'assessment',
    name: 'Assessment Guidelines',
    description: 'Evaluation criteria',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />'
  },
  {
    id: 'curriculum',
    name: 'Full Curriculum',
    description: 'Complete course structure',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />'
  }
]

// Industries
const industries = [
  { id: 'it', name: 'Information Technology' },
  { id: 'healthcare', name: 'Healthcare' },
  { id: 'manufacturing', name: 'Manufacturing' },
  { id: 'finance', name: 'Finance & Banking' },
  { id: 'education', name: 'Education & Training' },
  { id: 'hospitality', name: 'Hospitality & Tourism' },
  { id: 'construction', name: 'Construction' },
  { id: 'retail', name: 'Retail & Sales' },
  { id: 'automotive', name: 'Automotive' },
  { id: 'agriculture', name: 'Agriculture' }
]

// Skill levels
const skillLevels = [
  { id: 'beginner', name: 'Beginner' },
  { id: 'intermediate', name: 'Intermediate' },
  { id: 'advanced', name: 'Advanced' },
  { id: 'expert', name: 'Expert' }
]

// Generation progress
const generationProgress = reactive({
  show: false,
  steps: [
    { id: 1, name: 'Analyzing Requirements', description: 'Processing input parameters...', status: 'pending' },
    { id: 2, name: 'Generating Structure', description: 'Creating template framework...', status: 'pending' },
    { id: 3, name: 'AI Content Generation', description: 'Generating detailed content...', status: 'pending' },
    { id: 4, name: 'Quality Validation', description: 'Validating output quality...', status: 'pending' },
    { id: 5, name: 'Finalizing Template', description: 'Preparing final output...', status: 'pending' }
  ]
})

// Quick actions
const quickActions = [
  {
    id: 1,
    name: 'Import from PDF',
    description: 'Extract content from existing documents',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />',
    action: () => importFromPDF()
  },
  {
    id: 2,
    name: 'Bulk Generation',
    description: 'Generate multiple templates',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />',
    action: () => bulkGeneration()
  },
  {
    id: 3,
    name: 'AI Chat Help',
    description: 'Get help with template design',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />',
    action: () => router.push('/chat')
  },
  {
    id: 4,
    name: 'Export Options',
    description: 'Configure export formats',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />',
    action: () => configureExport()
  }
]

// Generation statistics
const generationStats = reactive([
  { id: 1, label: 'Templates Generated', value: '47', color: 'bg-blue-500' },
  { id: 2, label: 'This Month', value: '12', color: 'bg-green-500' },
  { id: 3, label: 'Success Rate', value: '98%', color: 'bg-purple-500' },
  { id: 4, label: 'Avg. Generation Time', value: '2.3m', color: 'bg-orange-500' }
])

// Recent templates
const recentTemplates = reactive([
  {
    id: 1,
    name: 'Python Programming NOSS',
    industry: 'IT',
    type: 'competency',
    createdAt: '2 hours ago'
  },
  {
    id: 2,
    name: 'Healthcare Assistant Assessment',
    industry: 'Healthcare',
    type: 'assessment',
    createdAt: '1 day ago'
  },
  {
    id: 3,
    name: 'Digital Marketing Curriculum',
    industry: 'IT',
    type: 'curriculum',
    createdAt: '3 days ago'
  }
])

// Template library
const templateLibrary = reactive([
  {
    id: 1,
    name: 'Software Development Fundamentals',
    description: 'Basic programming and software development skills',
    industry: 'IT',
    type: 'competency'
  },
  {
    id: 2,
    name: 'Network Administration',
    description: 'Network setup, maintenance, and troubleshooting',
    industry: 'IT',
    type: 'competency'
  },
  {
    id: 3,
    name: 'Patient Care Assessment',
    description: 'Healthcare patient care evaluation criteria',
    industry: 'Healthcare',
    type: 'assessment'
  },
  {
    id: 4,
    name: 'Manufacturing Quality Control',
    description: 'Quality assurance and control processes',
    industry: 'Manufacturing',
    type: 'competency'
  },
  {
    id: 5,
    name: 'Financial Analysis Curriculum',
    description: 'Complete financial analysis training program',
    industry: 'Finance',
    type: 'curriculum'
  },
  {
    id: 6,
    name: 'Hospitality Service Excellence',
    description: 'Customer service and hospitality management',
    industry: 'Hospitality',
    type: 'competency'
  }
])

// Generation history
const generationHistory = reactive([
  {
    id: 1,
    name: 'Web Development NOSS Template',
    industry: 'IT',
    type: 'Competency Units',
    createdAt: '2024-01-15',
    status: 'completed'
  },
  {
    id: 2,
    name: 'Nursing Assessment Guidelines',
    industry: 'Healthcare',
    type: 'Assessment Guidelines',
    createdAt: '2024-01-14',
    status: 'completed'
  },
  {
    id: 3,
    name: 'Manufacturing Safety Curriculum',
    industry: 'Manufacturing',
    type: 'Full Curriculum',
    createdAt: '2024-01-13',
    status: 'completed'
  }
])

// Computed
const canGenerate = computed(() => {
  return selectedTemplateType.value && selectedIndustry.value && selectedSkillLevel.value
})

// Methods
const generateTemplate = async () => {
  if (!canGenerate.value || isGenerating.value) return
  
  isGenerating.value = true
  generationProgress.show = true
  
  // Reset progress
  generationProgress.steps.forEach(step => step.status = 'pending')
  
  try {
    // Simulate generation process
    for (let i = 0; i < generationProgress.steps.length; i++) {
      generationProgress.steps[i].status = 'processing'
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
      generationProgress.steps[i].status = 'completed'
    }
    
    // Generate mock template content
    const templateType = templateTypes.find(t => t.id === selectedTemplateType.value)
    const industry = industries.find(i => i.id === selectedIndustry.value)
    const skillLevel = skillLevels.find(s => s.id === selectedSkillLevel.value)
    
    const mockTemplate = generateMockTemplate(templateType, industry, skillLevel)
    
    generatedTemplate.value = {
      id: Date.now(),
      name: `${industry.name} ${templateType.name}`,
      type: templateType.name,
      industry: industry.name,
      skillLevel: skillLevel.name,
      content: mockTemplate,
      createdAt: new Date().toISOString()
    }
    
    // Update statistics
    generationStats[0].value = (parseInt(generationStats[0].value) + 1).toString()
    generationStats[1].value = (parseInt(generationStats[1].value) + 1).toString()
    
    // Add to recent templates
    recentTemplates.unshift({
      id: Date.now(),
      name: generatedTemplate.value.name,
      industry: industry.name,
      type: templateType.id,
      createdAt: 'Just now'
    })
    
    appStore.addNotification({
      type: 'success',
      title: 'Template Generated',
      message: `${generatedTemplate.value.name} has been successfully generated`
    })
    
  } catch (error) {
    console.error('Template generation failed:', error)
    appStore.addNotification({
      type: 'error',
      title: 'Generation Failed',
      message: 'Failed to generate template. Please try again.'
    })
  } finally {
    isGenerating.value = false
    setTimeout(() => {
      generationProgress.show = false
    }, 2000)
  }
}

const generateMockTemplate = (templateType, industry, skillLevel) => {
  const baseContent = `# ${industry.name} ${templateType.name}

## Overview
This ${templateType.name.toLowerCase()} is designed for ${skillLevel.name.toLowerCase()}-level professionals in the ${industry.name.toLowerCase()} industry.

## Competency Units

### Unit 1: Core Knowledge
**Performance Criteria:**
- Demonstrate understanding of fundamental concepts
- Apply theoretical knowledge to practical situations
- Identify key industry standards and practices

**Knowledge Requirements:**
- Industry-specific terminology and concepts
- Regulatory requirements and compliance standards
- Best practices and quality standards

**Assessment Methods:**
- Written examination (40%)
- Practical demonstration (40%)
- Portfolio assessment (20%)

### Unit 2: Practical Application
**Performance Criteria:**
- Execute tasks according to industry standards
- Demonstrate problem-solving capabilities
- Work effectively in team environments

**Knowledge Requirements:**
- Technical procedures and protocols
- Safety requirements and risk management
- Tools, equipment, and technology usage

**Assessment Methods:**
- Hands-on practical assessment (60%)
- Case study analysis (25%)
- Peer evaluation (15%)

### Unit 3: Professional Development
**Performance Criteria:**
- Demonstrate continuous learning commitment
- Apply ethical principles in professional practice
- Communicate effectively with stakeholders

**Knowledge Requirements:**
- Professional ethics and standards
- Communication and interpersonal skills
- Industry trends and emerging technologies

**Assessment Methods:**
- Professional portfolio (50%)
- Presentation and discussion (30%)
- Self-reflection report (20%)

## Learning Outcomes
Upon completion of this ${templateType.name.toLowerCase()}, learners will be able to:
1. Apply core knowledge and skills in ${industry.name.toLowerCase()} contexts
2. Demonstrate competency in practical applications
3. Maintain professional standards and ethical practices
4. Adapt to changing industry requirements and technologies

## Quality Assurance
- Regular review and updates based on industry feedback
- Alignment with national and international standards
- Continuous improvement based on assessment outcomes
- Stakeholder consultation and validation

${customRequirements.value ? `\n## Additional Requirements\n${customRequirements.value}` : ''}

---
Generated using AI-powered NOSS Template Generator
Model: ${selectedAIModel.value}
Generated on: ${new Date().toLocaleDateString()}
`

  return baseContent
}

const editTemplate = () => {
  // TODO: Implement template editor
  appStore.addNotification({
    type: 'info',
    title: 'Coming Soon',
    message: 'Template editor functionality will be available soon'
  })
}

const saveTemplate = async () => {
  if (!generatedTemplate.value) return
  
  try {
    // TODO: Save to backend
    // Add to generation history
    generationHistory.unshift({
      id: Date.now(),
      name: generatedTemplate.value.name,
      industry: generatedTemplate.value.industry,
      type: generatedTemplate.value.type,
      createdAt: new Date().toISOString().split('T')[0],
      status: 'completed'
    })
    
    appStore.addNotification({
      type: 'success',
      title: 'Template Saved',
      message: `${generatedTemplate.value.name} has been saved successfully`
    })
  } catch (error) {
    appStore.addNotification({
      type: 'error',
      title: 'Save Failed',
      message: 'Failed to save template. Please try again.'
    })
  }
}

const downloadTemplate = () => {
  if (!generatedTemplate.value) return
  
  const blob = new Blob([generatedTemplate.value.content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${generatedTemplate.value.name.replace(/\s+/g, '_')}.txt`
  a.click()
  URL.revokeObjectURL(url)
  
  appStore.addNotification({
    type: 'success',
    title: 'Template Downloaded',
    message: 'Template has been downloaded successfully'
  })
}

const useTemplate = (template) => {
  selectedTemplateType.value = template.type
  selectedIndustry.value = template.industry
  customRequirements.value = `Based on template: ${template.name}\n${template.description}`
  showTemplateLibrary.value = false
  
  appStore.addNotification({
    type: 'info',
    title: 'Template Loaded',
    message: `Template "${template.name}" has been loaded`
  })
}

const loadTemplate = (template) => {
  // TODO: Load existing template for editing
  appStore.addNotification({
    type: 'info',
    title: 'Template Loaded',
    message: `Loading "${template.name}" for editing`
  })
}

const viewTemplate = (template) => {
  // TODO: View template details
  appStore.addNotification({
    type: 'info',
    title: 'Template View',
    message: `Viewing details for "${template.name}"`
  })
}

const deleteTemplate = (template) => {
  if (confirm(`Are you sure you want to delete "${template.name}"?`)) {
    const index = generationHistory.findIndex(t => t.id === template.id)
    if (index > -1) {
      generationHistory.splice(index, 1)
      appStore.addNotification({
        type: 'success',
        title: 'Template Deleted',
        message: `"${template.name}" has been deleted`
      })
    }
  }
}

const importFromPDF = () => {
  // TODO: Implement PDF import
  appStore.addNotification({
    type: 'info',
    title: 'Coming Soon',
    message: 'PDF import functionality will be available soon'
  })
}

const bulkGeneration = () => {
  // TODO: Implement bulk generation
  appStore.addNotification({
    type: 'info',
    title: 'Coming Soon',
    message: 'Bulk generation functionality will be available soon'
  })
}

const configureExport = () => {
  // TODO: Implement export configuration
  appStore.addNotification({
    type: 'info',
    title: 'Coming Soon',
    message: 'Export configuration will be available soon'
  })
}

// Initialize
onMounted(() => {
  // Load user preferences or recent settings
  // TODO: Load from API
})
</script>

<style scoped>
/* Custom scrollbar for modals */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400 dark:bg-gray-500;
}

/* Animation for progress steps */
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
