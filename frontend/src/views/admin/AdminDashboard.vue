<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Admin Dashboard</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              System overview and management tools
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="refreshData"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': isRefreshing }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh
            </button>
            <button
              @click="showSystemLogs = true"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              System Logs
            </button>
          </div>
        </div>
      </div>

      <!-- System Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div
          v-for="status in systemStatus"
          :key="status.id"
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg"
        >
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div :class="[
                  'w-8 h-8 rounded-md flex items-center justify-center',
                  status.status === 'healthy' ? 'bg-green-500' :
                  status.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'
                ]">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="status.icon"></svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">{{ status.name }}</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-gray-900 dark:text-white">{{ status.value }}</div>
                    <div :class="[
                      'ml-2 flex items-baseline text-sm font-semibold',
                      status.trend === 'up' ? 'text-green-600 dark:text-green-400' :
                      status.trend === 'down' ? 'text-red-600 dark:text-red-400' : 'text-gray-500'
                    ]">
                      <svg v-if="status.trend === 'up'" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                      </svg>
                      <svg v-else-if="status.trend === 'down'" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                      {{ status.change }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div :class="[
            'px-5 py-3',
            status.status === 'healthy' ? 'bg-green-50 dark:bg-green-900/20' :
            status.status === 'warning' ? 'bg-yellow-50 dark:bg-yellow-900/20' : 'bg-red-50 dark:bg-red-900/20'
          ]">
            <div class="text-sm">
              <a href="#" :class="[
                'font-medium',
                status.status === 'healthy' ? 'text-green-700 dark:text-green-300' :
                status.status === 'warning' ? 'text-yellow-700 dark:text-yellow-300' : 'text-red-700 dark:text-red-300'
              ]">
                {{ status.description }}
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content Area -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Quick Actions -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <router-link
                  v-for="action in quickActions"
                  :key="action.id"
                  :to="action.route"
                  class="relative group bg-white dark:bg-gray-700 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                >
                  <div>
                    <span :class="[
                      'rounded-lg inline-flex p-3 ring-4 ring-white dark:ring-gray-700',
                      action.bgColor
                    ]">
                      <svg :class="['w-6 h-6', action.iconColor]" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="action.icon"></svg>
                    </span>
                  </div>
                  <div class="mt-8">
                    <h3 class="text-lg font-medium text-gray-900 dark:text-white">
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      {{ action.name }}
                    </h3>
                    <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                      {{ action.description }}
                    </p>
                  </div>
                  <span class="pointer-events-none absolute top-6 right-6 text-gray-300 dark:text-gray-600 group-hover:text-gray-400 dark:group-hover:text-gray-500" aria-hidden="true">
                    <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                    </svg>
                  </span>
                </router-link>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">Recent Admin Activity</h3>
              <div class="flow-root">
                <ul role="list" class="-mb-8">
                  <li v-for="(activity, activityIdx) in recentActivity" :key="activity.id">
                    <div class="relative pb-8">
                      <span v-if="activityIdx !== recentActivity.length - 1" class="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200 dark:bg-gray-700" aria-hidden="true"></span>
                      <div class="relative flex items-start space-x-3">
                        <div class="relative">
                          <div :class="[
                            'h-10 w-10 rounded-full flex items-center justify-center ring-8 ring-white dark:ring-gray-800',
                            activity.type === 'success' ? 'bg-green-500' :
                            activity.type === 'warning' ? 'bg-yellow-500' :
                            activity.type === 'error' ? 'bg-red-500' : 'bg-blue-500'
                          ]">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="activity.icon"></svg>
                          </div>
                        </div>
                        <div class="min-w-0 flex-1">
                          <div>
                            <div class="text-sm">
                              <span class="font-medium text-gray-900 dark:text-white">{{ activity.user }}</span>
                            </div>
                            <p class="mt-0.5 text-sm text-gray-500 dark:text-gray-400">{{ activity.action }}</p>
                          </div>
                          <div class="mt-2 text-sm text-gray-700 dark:text-gray-300">
                            <p>{{ activity.details }}</p>
                          </div>
                          <div class="mt-2">
                            <span class="text-xs text-gray-500 dark:text-gray-400">{{ activity.timestamp }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- System Performance Chart -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">System Performance</h3>
              <div class="space-y-4">
                <div v-for="metric in performanceMetrics" :key="metric.id">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-500 dark:text-gray-400">{{ metric.name }}</span>
                    <span class="font-medium text-gray-900 dark:text-white">{{ metric.value }}%</span>
                  </div>
                  <div class="mt-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      :class="[
                        'h-2 rounded-full transition-all duration-300',
                        metric.value >= 80 ? 'bg-green-500' :
                        metric.value >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                      ]"
                      :style="{ width: `${metric.value}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- System Stats -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">System Statistics</h3>
              <dl class="space-y-4">
                <div v-for="stat in systemStats" :key="stat.id" class="flex justify-between">
                  <dt class="text-sm text-gray-500 dark:text-gray-400">{{ stat.label }}</dt>
                  <dd class="text-sm font-medium text-gray-900 dark:text-white">{{ stat.value }}</dd>
                </div>
              </dl>
            </div>
          </div>

          <!-- AI Service Status -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">AI Services</h3>
              <div class="space-y-3">
                <div v-for="service in aiServices" :key="service.id" class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div :class="[
                      'w-2 h-2 rounded-full mr-3',
                      service.status === 'online' ? 'bg-green-500' :
                      service.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'
                    ]"></div>
                    <span class="text-sm text-gray-900 dark:text-white">{{ service.name }}</span>
                  </div>
                  <span class="text-xs text-gray-500 dark:text-gray-400">{{ service.latency }}ms</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Alerts -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">System Alerts</h3>
              <div class="space-y-3">
                <div v-for="alert in systemAlerts" :key="alert.id" :class="[
                  'p-3 rounded-lg border-l-4',
                  alert.level === 'error' ? 'bg-red-50 dark:bg-red-900/20 border-red-400' :
                  alert.level === 'warning' ? 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-400' :
                  'bg-blue-50 dark:bg-blue-900/20 border-blue-400'
                ]">
                  <div class="flex">
                    <div class="flex-shrink-0">
                      <svg :class="[
                        'h-5 w-5',
                        alert.level === 'error' ? 'text-red-400' :
                        alert.level === 'warning' ? 'text-yellow-400' : 'text-blue-400'
                      ]" fill="currentColor" viewBox="0 0 20 20" v-html="alert.icon"></svg>
                    </div>
                    <div class="ml-3">
                      <p :class="[
                        'text-sm font-medium',
                        alert.level === 'error' ? 'text-red-800 dark:text-red-200' :
                        alert.level === 'warning' ? 'text-yellow-800 dark:text-yellow-200' :
                        'text-blue-800 dark:text-blue-200'
                      ]">
                        {{ alert.title }}
                      </p>
                      <p :class="[
                        'mt-1 text-sm',
                        alert.level === 'error' ? 'text-red-700 dark:text-red-300' :
                        alert.level === 'warning' ? 'text-yellow-700 dark:text-yellow-300' :
                        'text-blue-700 dark:text-blue-300'
                      ]">
                        {{ alert.message }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Maintenance Window -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">Maintenance</h3>
              <div class="space-y-3">
                <button
                  @click="showMaintenanceModal = true"
                  class="w-full text-left p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">System Maintenance</span>
                  </div>
                  <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Schedule maintenance windows</p>
                </button>
                <button
                  @click="clearCache"
                  class="w-full text-left p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Clear System Cache</span>
                  </div>
                  <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Clear all cached data</p>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Logs Modal -->
    <div v-if="showSystemLogs" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showSystemLogs = false">
      <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-6xl shadow-lg rounded-md bg-white dark:bg-gray-800" @click.stop>
        <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">System Logs</h3>
          <button @click="showSystemLogs = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-4 max-h-96 overflow-y-auto">
          <div class="bg-gray-900 text-green-400 font-mono text-sm p-4 rounded-lg">
            <div v-for="log in systemLogs" :key="log.id" class="mb-1">
              <span class="text-gray-500">[{{ log.timestamp }}]</span>
              <span :class="[
                log.level === 'error' ? 'text-red-400' :
                log.level === 'warning' ? 'text-yellow-400' :
                log.level === 'info' ? 'text-blue-400' : 'text-green-400'
              ]">[{{ log.level.toUpperCase() }}]</span>
              <span class="text-gray-300">{{ log.message }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Maintenance Modal -->
    <div v-if="showMaintenanceModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showMaintenanceModal = false">
      <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-md shadow-lg rounded-md bg-white dark:bg-gray-800" @click.stop>
        <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Schedule Maintenance</h3>
          <button @click="showMaintenanceModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mt-4">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            This feature will be available in a future update. For now, please contact the system administrator for maintenance scheduling.
          </p>
          <button
            @click="showMaintenanceModal = false"
            class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useAppStore } from '../../store'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

// Reactive data
const isRefreshing = ref(false)
const showSystemLogs = ref(false)
const showMaintenanceModal = ref(false)

// System status
const systemStatus = reactive([
  {
    id: 1,
    name: 'Database',
    value: 'Online',
    status: 'healthy',
    trend: 'stable',
    change: '99.9%',
    description: 'All database connections healthy',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />'
  },
  {
    id: 2,
    name: 'AI Services',
    value: '3/3',
    status: 'healthy',
    trend: 'up',
    change: '+2.1%',
    description: 'All AI models responding',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />'
  },
  {
    id: 3,
    name: 'API Response',
    value: '124ms',
    status: 'healthy',
    trend: 'down',
    change: '-12ms',
    description: 'Optimal response times',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />'
  },
  {
    id: 4,
    name: 'Storage',
    value: '73%',
    status: 'warning',
    trend: 'up',
    change: '+5%',
    description: 'Monitor disk usage',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />'
  }
])

// Quick actions
const quickActions = [
  {
    id: 1,
    name: 'User Management',
    description: 'Manage user accounts and permissions',
    route: '/admin/users',
    bgColor: 'bg-blue-500',
    iconColor: 'text-white',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 0a6 6 0 01-3 5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />'
  },
  {
    id: 2,
    name: 'Document Management',
    description: 'Manage documents and templates',
    route: '/admin/documents',
    bgColor: 'bg-green-500',
    iconColor: 'text-white',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />'
  },
  {
    id: 3,
    name: 'Template Management',
    description: 'Manage NOSS templates and configurations',
    route: '/admin/templates',
    bgColor: 'bg-purple-500',
    iconColor: 'text-white',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />'
  },
  {
    id: 4,
    name: 'Chat History',
    description: 'Monitor AI chat interactions',
    route: '/admin/chat-history',
    bgColor: 'bg-yellow-500',
    iconColor: 'text-white',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />'
  },
  {
    id: 5,
    name: 'Token Usage',
    description: 'Monitor AI token consumption',
    route: '/admin/token-usage',
    bgColor: 'bg-red-500',
    iconColor: 'text-white',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />'
  },
  {
    id: 6,
    name: 'Metadata Management',
    description: 'Manage system metadata and configurations',
    route: '/admin/metadata',
    bgColor: 'bg-indigo-500',
    iconColor: 'text-white',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />'
  }
]

// Recent activity
const recentActivity = reactive([
  {
    id: 1,
    user: 'System Admin',
    action: 'Template generation completed',
    details: 'Generated new IT competency template for Python programming',
    timestamp: '2 minutes ago',
    type: 'success',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />'
  },
  {
    id: 2,
    user: 'Jane Smith',
    action: 'User login',
    details: 'Successful authentication from IP 192.168.1.100',
    timestamp: '5 minutes ago',
    type: 'info',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />'
  },
  {
    id: 3,
    user: 'AI Service',
    action: 'High token usage detected',
    details: 'GPT-4 usage approaching daily limit (85% consumed)',
    timestamp: '10 minutes ago',
    type: 'warning',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />'
  },
  {
    id: 4,
    user: 'System',
    action: 'Database backup completed',
    details: 'Automated daily backup completed successfully (2.3GB)',
    timestamp: '1 hour ago',
    type: 'success',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />'
  },
  {
    id: 5,
    user: 'John Doe',
    action: 'Document upload failed',
    details: 'PDF processing failed due to corrupted file format',
    timestamp: '2 hours ago',
    type: 'error',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />'
  }
])

// Performance metrics
const performanceMetrics = reactive([
  { id: 1, name: 'CPU Usage', value: 35 },
  { id: 2, name: 'Memory Usage', value: 68 },
  { id: 3, name: 'Disk I/O', value: 42 },
  { id: 4, name: 'Network Throughput', value: 78 }
])

// System statistics
const systemStats = reactive([
  { id: 1, label: 'Total Users', value: '1,247' },
  { id: 2, label: 'Active Sessions', value: '89' },
  { id: 3, label: 'Documents Processed', value: '3,456' },
  { id: 4, label: 'Templates Generated', value: '892' },
  { id: 5, label: 'AI Queries Today', value: '1,234' },
  { id: 6, label: 'Storage Used', value: '847 GB' },
  { id: 7, label: 'Uptime', value: '99.8%' },
  { id: 8, label: 'Response Time', value: '124ms' }
])

// AI services
const aiServices = reactive([
  { id: 1, name: 'GPT-4', status: 'online', latency: 156 },
  { id: 2, name: 'GPT-3.5', status: 'online', latency: 89 },
  { id: 3, name: 'Claude-3', status: 'online', latency: 203 }
])

// System alerts
const systemAlerts = reactive([
  {
    id: 1,
    level: 'warning',
    title: 'High Storage Usage',
    message: 'Disk usage is at 73%. Consider cleanup or expansion.',
    icon: '<path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />'
  },
  {
    id: 2,
    level: 'info',
    title: 'Scheduled Maintenance',
    message: 'System maintenance scheduled for tonight at 2:00 AM.',
    icon: '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />'
  }
])

// System logs
const systemLogs = reactive([
  {
    id: 1,
    timestamp: '2024-01-15 14:23:45',
    level: 'info',
    message: 'User authentication successful for user: jane.smith@example.com'
  },
  {
    id: 2,
    timestamp: '2024-01-15 14:22:31',
    level: 'success',
    message: 'Template generation completed successfully (ID: TPL-789)'
  },
  {
    id: 3,
    timestamp: '2024-01-15 14:21:15',
    level: 'warning',
    message: 'High CPU usage detected: 89% utilization'
  },
  {
    id: 4,
    timestamp: '2024-01-15 14:20:02',
    level: 'error',
    message: 'Failed to process document upload: Invalid file format'
  },
  {
    id: 5,
    timestamp: '2024-01-15 14:19:48',
    level: 'info',
    message: 'Database backup initiated'
  },
  {
    id: 6,
    timestamp: '2024-01-15 14:18:33',
    level: 'success',
    message: 'AI service health check completed - all services operational'
  }
])

// Methods
const refreshData = async () => {
  isRefreshing.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update metrics with random variations
    performanceMetrics.forEach(metric => {
      const change = Math.floor(Math.random() * 20) - 10
      metric.value = Math.max(0, Math.min(100, metric.value + change))
    })
    
    appStore.addNotification({
      type: 'success',
      title: 'Data Refreshed',
      message: 'Dashboard data has been updated'
    })
  } catch (error) {
    appStore.addNotification({
      type: 'error',
      title: 'Refresh Failed',
      message: 'Failed to refresh dashboard data'
    })
  } finally {
    isRefreshing.value = false
  }
}

const clearCache = async () => {
  if (confirm('Are you sure you want to clear the system cache? This may temporarily slow down the application.')) {
    try {
      // TODO: Implement cache clearing
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      appStore.addNotification({
        type: 'success',
        title: 'Cache Cleared',
        message: 'System cache has been cleared successfully'
      })
    } catch (error) {
      appStore.addNotification({
        type: 'error',
        title: 'Cache Clear Failed',
        message: 'Failed to clear system cache'
      })
    }
  }
}

// Initialize
onMounted(() => {
  // TODO: Load dashboard data from API
})
</script>

<style scoped>
/* Custom animations for charts and metrics */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in {
  animation: slideIn 0.3s ease-out;
}

/* Hover effects for quick actions */
.group:hover .pointer-events-none {
  @apply text-gray-400 dark:text-gray-500;
}
</style>
