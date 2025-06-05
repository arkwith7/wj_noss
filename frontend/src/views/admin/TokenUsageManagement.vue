<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Token Usage Management</h1>
        <p class="text-gray-600 dark:text-gray-400">Monitor AI token consumption, costs, and usage patterns</p>
      </div>
      <div class="flex space-x-3">
        <button @click="showUsageLimitsModal = true" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4a2 2 0 100-4m6 4a2 2 0 100-4m0 4a2 2 0 100 4m0-4a2 2 0 100-4m6-8a2 2 0 100-4m0 4a2 2 0 100 4m0-4a2 2 0 100-4" />
          </svg>
          Manage Limits
        </button>
        <button @click="exportUsageReport" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Export Report
        </button>
      </div>
    </div>

    <!-- Current Usage Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Tokens Used Today</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ formatTokens(usageStats.tokensToday) }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ usageStats.percentageOfDaily }}% of daily limit</p>
          </div>
        </div>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div :style="{ width: usageStats.percentageOfDaily + '%' }" class="bg-blue-600 h-2 rounded-full"></div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 dark:bg-green-900">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Cost Today</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">${{ usageStats.costToday }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ usageStats.percentageOfBudget }}% of budget</p>
          </div>
        </div>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div :style="{ width: usageStats.percentageOfBudget + '%' }" class="bg-green-600 h-2 rounded-full"></div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Usage</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ formatTokens(usageStats.tokensMonth) }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ usageStats.percentageOfMonthly }}% of monthly limit</p>
          </div>
        </div>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div :style="{ width: usageStats.percentageOfMonthly + '%' }" class="bg-purple-600 h-2 rounded-full"></div>
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
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Avg Response Time</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ usageStats.avgResponseTime }}s</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Across all models</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Usage Over Time -->
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Token Usage Over Time</h3>
          <select v-model="selectedPeriod" class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm">
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
          </select>
        </div>
        <div class="h-64 bg-gray-50 dark:bg-gray-900 rounded-lg p-4 flex items-center justify-center">
          <span class="text-gray-500 dark:text-gray-400">Usage chart would be displayed here</span>
        </div>
      </div>

      <!-- Model Distribution -->
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">Usage by Model</h3>
        <div class="space-y-4">
          <div v-for="model in modelUsage" :key="model.name" class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div :class="model.color" class="w-3 h-3 rounded-full"></div>
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ model.name }}</span>
            </div>
            <div class="flex items-center space-x-4">
              <div class="text-right">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{{ formatTokens(model.tokens) }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">${{ model.cost }}</div>
              </div>
              <div class="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div :style="{ width: model.percentage + '%' }" :class="model.color.replace('bg-', 'bg-')" class="h-2 rounded-full"></div>
              </div>
              <span class="text-sm text-gray-500 dark:text-gray-400 w-12">{{ model.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Limits and Alerts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Current Limits -->
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Usage Limits</h3>
          <button @click="showUsageLimitsModal = true" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 text-sm">
            Edit Limits
          </button>
        </div>
        <div class="space-y-4">
          <div v-for="limit in usageLimits" :key="limit.type" class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div>
              <div class="font-medium text-gray-900 dark:text-white">{{ limit.name }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ limit.description }}</div>
            </div>
            <div class="text-right">
              <div class="font-medium text-gray-900 dark:text-white">{{ formatTokens(limit.limit) }}</div>
              <div class="text-sm" :class="getUsageColor(limit.currentUsage, limit.limit)">
                {{ formatTokens(limit.currentUsage) }} used
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Alerts and Notifications -->
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">Recent Alerts</h3>
        <div class="space-y-3">
          <div v-for="alert in recentAlerts" :key="alert.id" :class="getAlertClass(alert.type)" class="p-4 rounded-lg">
            <div class="flex items-start">
              <svg v-if="alert.type === 'warning'" class="w-5 h-5 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="alert.type === 'error'" class="w-5 h-5 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="w-5 h-5 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              <div class="flex-1">
                <div class="font-medium">{{ alert.title }}</div>
                <div class="text-sm opacity-75">{{ alert.message }}</div>
                <div class="text-xs opacity-60 mt-1">{{ formatDate(alert.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Usage Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">User Token Usage</h3>
          <div class="flex items-center space-x-4">
            <select v-model="userSortBy" class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm">
              <option value="tokens">Sort by Tokens</option>
              <option value="cost">Sort by Cost</option>
              <option value="name">Sort by Name</option>
            </select>
            <div class="relative">
              <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                v-model="userSearchQuery"
                type="text"
                placeholder="Search users..."
                class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
              >
            </div>
          </div>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">User</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Tokens Used</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Cost</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Chats</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Avg per Chat</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Last Activity</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                    <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {{ user.name.charAt(0).toUpperCase() }}
                    </span>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ user.name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{{ formatTokens(user.tokensUsed) }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">{{ user.percentageOfTotal }}% of total</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                ${{ user.cost }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ user.chatCount }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ formatTokens(user.avgTokensPerChat) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ formatDate(user.lastActivity) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button @click="viewUserDetails(user)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button @click="setUserLimit(user)" class="text-orange-600 hover:text-orange-900 dark:text-orange-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4a2 2 0 100-4m6 4a2 2 0 100-4m0 4a2 2 0 100 4m0-4a2 2 0 100-4m6-8a2 2 0 100-4m0 4a2 2 0 100 4m0-4a2 2 0 100-4" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Usage Limits Modal -->
    <div v-if="showUsageLimitsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Manage Usage Limits</h3>
          <button @click="showUsageLimitsModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveUsageLimits" class="space-y-6">
          <div v-for="limit in editableLimits" :key="limit.type" class="space-y-3">
            <div class="flex items-center justify-between">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">{{ limit.name }}</label>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ limit.description }}</p>
              </div>
              <div class="flex items-center space-x-2">
                <input
                  v-model="limit.limit"
                  type="number"
                  class="w-24 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                <select
                  v-model="limit.unit"
                  class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  <option value="tokens">Tokens</option>
                  <option value="k">K Tokens</option>
                  <option value="m">M Tokens</option>
                </select>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <input
                v-model="limit.alertEnabled"
                type="checkbox"
                class="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
              >
              <label class="text-sm text-gray-700 dark:text-gray-300">
                Send alert at
              </label>
              <input
                v-model="limit.alertThreshold"
                type="number"
                min="1"
                max="100"
                class="w-16 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
              >
              <span class="text-sm text-gray-500 dark:text-gray-400">% of limit</span>
            </div>
          </div>

          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="showUsageLimitsModal = false"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Save Limits
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
  name: 'TokenUsageManagement',
  setup() {
    // Reactive data
    const selectedPeriod = ref('30')
    const userSortBy = ref('tokens')
    const userSearchQuery = ref('')
    const showUsageLimitsModal = ref(false)
    const userUsage = ref([])
    
    // Usage statistics
    const usageStats = ref({
      tokensToday: 125000,
      percentageOfDaily: 62,
      costToday: 18.50,
      percentageOfBudget: 37,
      tokensMonth: 2400000,
      percentageOfMonthly: 48,
      avgResponseTime: 2.3
    })

    // Model usage data
    const modelUsage = ref([
      {
        name: 'GPT-4',
        tokens: 1200000,
        cost: 120.50,
        percentage: 45,
        color: 'bg-blue-500'
      },
      {
        name: 'GPT-3.5 Turbo',
        tokens: 980000,
        cost: 42.80,
        percentage: 38,
        color: 'bg-green-500'
      },
      {
        name: 'Claude 3',
        tokens: 420000,
        cost: 28.40,
        percentage: 17,
        color: 'bg-purple-500'
      }
    ])

    // Usage limits
    const usageLimits = ref([
      {
        type: 'daily',
        name: 'Daily Limit',
        description: 'Maximum tokens per day',
        limit: 200000,
        currentUsage: 125000
      },
      {
        type: 'monthly',
        name: 'Monthly Limit',
        description: 'Maximum tokens per month',
        limit: 5000000,
        currentUsage: 2400000
      },
      {
        type: 'user',
        name: 'Per User Daily',
        description: 'Maximum tokens per user per day',
        limit: 10000,
        currentUsage: 8500
      }
    ])

    // Editable limits for modal
    const editableLimits = ref([
      {
        type: 'daily',
        name: 'Daily Limit',
        description: 'Maximum tokens per day across all users',
        limit: 200,
        unit: 'k',
        alertEnabled: true,
        alertThreshold: 80
      },
      {
        type: 'monthly',
        name: 'Monthly Limit',
        description: 'Maximum tokens per month across all users',
        limit: 5,
        unit: 'm',
        alertEnabled: true,
        alertThreshold: 90
      },
      {
        type: 'user_daily',
        name: 'User Daily Limit',
        description: 'Maximum tokens per user per day',
        limit: 10,
        unit: 'k',
        alertEnabled: true,
        alertThreshold: 75
      },
      {
        type: 'user_monthly',
        name: 'User Monthly Limit',
        description: 'Maximum tokens per user per month',
        limit: 250,
        unit: 'k',
        alertEnabled: false,
        alertThreshold: 80
      }
    ])

    // Recent alerts
    const recentAlerts = ref([
      {
        id: 1,
        type: 'warning',
        title: 'Daily Usage Alert',
        message: 'Daily token usage has reached 80% of the limit',
        timestamp: '2024-02-15T14:30:00Z'
      },
      {
        id: 2,
        type: 'info',
        title: 'High User Activity',
        message: 'User John Doe has exceeded their daily recommendation',
        timestamp: '2024-02-15T12:15:00Z'
      },
      {
        id: 3,
        type: 'error',
        title: 'Rate Limit Exceeded',
        message: 'API rate limit temporarily exceeded for GPT-4',
        timestamp: '2024-02-15T10:45:00Z'
      }
    ])

    // Computed properties
    const filteredUsers = computed(() => {
      let filtered = userUsage.value.filter(user => 
        user.name.toLowerCase().includes(userSearchQuery.value.toLowerCase()) ||
        user.email.toLowerCase().includes(userSearchQuery.value.toLowerCase())
      )

      // Sort users
      filtered.sort((a, b) => {
        switch (userSortBy.value) {
          case 'tokens':
            return b.tokensUsed - a.tokensUsed
          case 'cost':
            return parseFloat(b.cost) - parseFloat(a.cost)
          case 'name':
            return a.name.localeCompare(b.name)
          default:
            return 0
        }
      })

      return filtered
    })

    // Methods
    const loadUserUsage = () => {
      // TODO: Replace with actual API call
      userUsage.value = [
        {
          id: 1,
          name: 'John Doe',
          email: 'john@example.com',
          tokensUsed: 45000,
          cost: 23.50,
          chatCount: 28,
          avgTokensPerChat: 1607,
          percentageOfTotal: 12.5,
          lastActivity: '2024-02-15T16:30:00Z'
        },
        {
          id: 2,
          name: 'Jane Smith',
          email: 'jane@example.com',
          tokensUsed: 38000,
          cost: 19.80,
          chatCount: 22,
          avgTokensPerChat: 1727,
          percentageOfTotal: 10.8,
          lastActivity: '2024-02-15T15:45:00Z'
        },
        {
          id: 3,
          name: 'Mike Johnson',
          email: 'mike@example.com',
          tokensUsed: 32000,
          cost: 16.20,
          chatCount: 19,
          avgTokensPerChat: 1684,
          percentageOfTotal: 9.2,
          lastActivity: '2024-02-15T14:20:00Z'
        },
        {
          id: 4,
          name: 'Sarah Wilson',
          email: 'sarah@example.com',
          tokensUsed: 28000,
          cost: 14.10,
          chatCount: 15,
          avgTokensPerChat: 1867,
          percentageOfTotal: 8.1,
          lastActivity: '2024-02-15T13:10:00Z'
        },
        {
          id: 5,
          name: 'David Brown',
          email: 'david@example.com',
          tokensUsed: 25000,
          cost: 12.75,
          chatCount: 18,
          avgTokensPerChat: 1389,
          percentageOfTotal: 7.2,
          lastActivity: '2024-02-15T12:30:00Z'
        }
      ]
    }

    const formatTokens = (tokens) => {
      if (tokens >= 1000000) {
        return (tokens / 1000000).toFixed(1) + 'M'
      } else if (tokens >= 1000) {
        return (tokens / 1000).toFixed(1) + 'K'
      }
      return tokens.toString()
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getUsageColor = (current, limit) => {
      const percentage = (current / limit) * 100
      if (percentage >= 90) return 'text-red-600 dark:text-red-400'
      if (percentage >= 75) return 'text-orange-600 dark:text-orange-400'
      if (percentage >= 50) return 'text-yellow-600 dark:text-yellow-400'
      return 'text-green-600 dark:text-green-400'
    }

    const getAlertClass = (type) => {
      switch (type) {
        case 'warning':
          return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
        case 'error':
          return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
        case 'info':
        default:
          return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
      }
    }

    const viewUserDetails = (user) => {
      // TODO: Implement user details modal
      console.log('View user details:', user)
    }

    const setUserLimit = (user) => {
      // TODO: Implement user limit setting
      console.log('Set user limit:', user)
    }

    const saveUsageLimits = () => {
      // TODO: Save limits via API
      console.log('Saving usage limits:', editableLimits.value)
      showUsageLimitsModal.value = false
    }

    const exportUsageReport = () => {
      // TODO: Generate and download usage report
      console.log('Exporting usage report')
    }

    // Lifecycle
    onMounted(() => {
      loadUserUsage()
    })

    return {
      // Data
      selectedPeriod,
      userSortBy,
      userSearchQuery,
      showUsageLimitsModal,
      usageStats,
      modelUsage,
      usageLimits,
      editableLimits,
      recentAlerts,
      userUsage,
      
      // Computed
      filteredUsers,
      
      // Methods
      formatTokens,
      formatDate,
      getUsageColor,
      getAlertClass,
      viewUserDetails,
      setUserLimit,
      saveUsageLimits,
      exportUsageReport
    }
  }
}
</script>
