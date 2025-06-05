<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Chat History Management</h1>
        <p class="text-gray-600 dark:text-gray-400">Monitor and manage AI chat conversations and interactions</p>
      </div>
      <div class="flex space-x-3">
        <button @click="exportChatData" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Export Data
        </button>
        <button @click="showAnalyticsModal = true" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Analytics
        </button>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Chats</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ chatStats.totalChats }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 dark:bg-green-900">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a2 2 0 01-2-2v-6a2 2 0 012-2h2V4a2 2 0 012-2h4a2 2 0 012 2v4z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Messages Today</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ chatStats.messagesToday }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Users</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ chatStats.activeUsers }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100 dark:bg-orange-900">
            <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Avg Response Time</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ chatStats.avgResponseTime }}s</p>
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
              placeholder="Search conversations..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
          </div>
        </div>
        <div class="flex gap-4">
          <select v-model="selectedUser" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white">
            <option value="">All Users</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.name }}</option>
          </select>
          <select v-model="selectedModel" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white">
            <option value="">All Models</option>
            <option value="gpt-4">GPT-4</option>
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            <option value="claude-3">Claude 3</option>
          </select>
          <input
            v-model="dateRange.start"
            type="date"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          >
          <input
            v-model="dateRange.end"
            type="date"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          >
        </div>
      </div>
    </div>

    <!-- Chat Conversations -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Chat Conversations</h3>
          <div class="flex items-center space-x-2">
            <button @click="selectAll" class="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400">
              {{ selectedChats.length === filteredChats.length ? 'Deselect All' : 'Select All' }}
            </button>
            <span class="text-gray-300 dark:text-gray-600">|</span>
            <div class="flex space-x-2">
              <button 
                @click="bulkExport"
                :disabled="selectedChats.length === 0"
                class="text-sm text-green-600 hover:text-green-800 dark:text-green-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Export Selected
              </button>
              <button 
                @click="bulkArchive"
                :disabled="selectedChats.length === 0"
                class="text-sm text-orange-600 hover:text-orange-800 dark:text-orange-400 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Archive Selected
              </button>
              <button 
                @click="bulkDelete"
                :disabled="selectedChats.length === 0"
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
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">User</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Conversation</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Model</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Messages</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Tokens</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Duration</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Created</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="chat in paginatedChats" :key="chat.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap">
                <input 
                  type="checkbox" 
                  :value="chat.id"
                  v-model="selectedChats"
                  class="rounded border-gray-300 dark:border-gray-600"
                >
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                    <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {{ chat.user.name.charAt(0).toUpperCase() }}
                    </span>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ chat.user.name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ chat.user.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900 dark:text-white font-medium">{{ chat.title }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate">
                  {{ chat.lastMessage }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getModelClass(chat.model)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ chat.model }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ chat.messageCount }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ formatTokens(chat.totalTokens) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ formatDuration(chat.duration) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ formatDate(chat.createdAt) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button @click="viewChat(chat)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button @click="exportChat(chat)" class="text-green-600 hover:text-green-900 dark:text-green-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </button>
                  <button @click="deleteChat(chat)" class="text-red-600 hover:text-red-900 dark:text-red-400">
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
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredChats.length) }} of {{ filteredChats.length }} conversations
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

    <!-- Chat View Modal -->
    <div v-if="showChatModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-hidden">
        <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ selectedChat?.title }}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ selectedChat?.user.name }} • {{ selectedChat?.messageCount }} messages • {{ formatDate(selectedChat?.createdAt) }}
            </p>
          </div>
          <button @click="showChatModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="p-6 overflow-y-auto max-h-[60vh]">
          <div class="space-y-4">
            <div v-for="message in selectedChat?.messages" :key="message.id" class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <div v-if="message.role === 'user'" class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                  <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div v-else class="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                  <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
              </div>
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-1">
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ message.role === 'user' ? 'User' : 'AI Assistant' }}
                  </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatTime(message.timestamp) }}
                  </span>
                </div>
                <div class="prose prose-sm dark:prose-invert max-w-none">
                  <p>{{ message.content }}</p>
                </div>
                <div v-if="message.tokens" class="mt-2 text-xs text-gray-500 dark:text-gray-400">
                  Tokens: {{ message.tokens }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytics Modal -->
    <div v-if="showAnalyticsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Chat Analytics</h3>
          <button @click="showAnalyticsModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="p-6 space-y-6">
          <!-- Usage Over Time -->
          <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Usage Over Time</h4>
            <div class="h-64 bg-white dark:bg-gray-800 rounded-lg p-4 flex items-center justify-center">
              <span class="text-gray-500 dark:text-gray-400">Chart placeholder - Usage trends would be displayed here</span>
            </div>
          </div>

          <!-- Model Usage -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Model Usage</h4>
              <div class="space-y-3">
                <div v-for="model in modelUsage" :key="model.name" class="flex items-center justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">{{ model.name }}</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div :style="{ width: model.percentage + '%' }" class="bg-blue-600 h-2 rounded-full"></div>
                    </div>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">{{ model.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Top Users</h4>
              <div class="space-y-3">
                <div v-for="user in topUsers" :key="user.id" class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                      <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                        {{ user.name.charAt(0).toUpperCase() }}
                      </span>
                    </div>
                    <span class="text-sm text-gray-900 dark:text-white">{{ user.name }}</span>
                  </div>
                  <span class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ user.messageCount }} messages</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Token Usage -->
          <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Token Usage Analysis</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-white dark:bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ tokenAnalysis.totalTokens }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Total Tokens</div>
              </div>
              <div class="bg-white dark:bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ tokenAnalysis.avgPerChat }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Avg per Chat</div>
              </div>
              <div class="bg-white dark:bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">${{ tokenAnalysis.estimatedCost }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Estimated Cost</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'ChatHistoryManagement',
  setup() {
    // Reactive data
    const chats = ref([])
    const users = ref([])
    const selectedChats = ref([])
    const searchQuery = ref('')
    const selectedUser = ref('')
    const selectedModel = ref('')
    const dateRange = ref({ start: '', end: '' })
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    
    // Modals
    const showChatModal = ref(false)
    const showAnalyticsModal = ref(false)
    const selectedChat = ref(null)

    // Statistics
    const chatStats = ref({
      totalChats: 1247,
      messagesToday: 189,
      activeUsers: 84,
      avgResponseTime: 2.3
    })

    // Analytics data
    const modelUsage = ref([
      { name: 'GPT-4', percentage: 45 },
      { name: 'GPT-3.5 Turbo', percentage: 38 },
      { name: 'Claude 3', percentage: 17 }
    ])

    const topUsers = ref([
      { id: 1, name: 'John Doe', messageCount: 234 },
      { id: 2, name: 'Jane Smith', messageCount: 189 },
      { id: 3, name: 'Mike Johnson', messageCount: 156 },
      { id: 4, name: 'Sarah Wilson', messageCount: 142 },
      { id: 5, name: 'David Brown', messageCount: 128 }
    ])

    const tokenAnalysis = ref({
      totalTokens: '2.4M',
      avgPerChat: '1,923',
      estimatedCost: '486.50'
    })

    // Computed properties
    const filteredChats = computed(() => {
      return chats.value.filter(chat => {
        const matchesSearch = !searchQuery.value || 
          chat.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          chat.user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          chat.lastMessage.toLowerCase().includes(searchQuery.value.toLowerCase())
        
        const matchesUser = !selectedUser.value || chat.user.id === selectedUser.value
        const matchesModel = !selectedModel.value || chat.model === selectedModel.value
        
        let matchesDate = true
        if (dateRange.value.start || dateRange.value.end) {
          const chatDate = new Date(chat.createdAt).toISOString().split('T')[0]
          if (dateRange.value.start && chatDate < dateRange.value.start) matchesDate = false
          if (dateRange.value.end && chatDate > dateRange.value.end) matchesDate = false
        }
        
        return matchesSearch && matchesUser && matchesModel && matchesDate
      })
    })

    const paginatedChats = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredChats.value.slice(start, end)
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredChats.value.length / itemsPerPage.value)
    })

    // Methods
    const loadChats = () => {
      // TODO: Replace with actual API call
      chats.value = [
        {
          id: 1,
          title: 'Healthcare Competency Discussion',
          user: { id: 1, name: 'John Doe', email: 'john@example.com' },
          model: 'gpt-4',
          messageCount: 15,
          totalTokens: 3247,
          duration: 1847, // seconds
          lastMessage: 'Thank you for helping me understand the healthcare competency framework.',
          createdAt: '2024-02-15T10:30:00Z',
          messages: [
            {
              id: 1,
              role: 'user',
              content: 'Can you help me understand the healthcare competency framework?',
              timestamp: '2024-02-15T10:30:00Z',
              tokens: 156
            },
            {
              id: 2,
              role: 'assistant',
              content: 'I\'d be happy to help you understand the healthcare competency framework. The framework consists of several key components including technical skills, patient care, communication, professionalism, and continuous learning.',
              timestamp: '2024-02-15T10:30:15Z',
              tokens: 234
            }
          ]
        },
        {
          id: 2,
          title: 'Technology Assessment Guidelines',
          user: { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
          model: 'gpt-3.5-turbo',
          messageCount: 8,
          totalTokens: 1923,
          duration: 1234,
          lastMessage: 'The assessment criteria you provided are very comprehensive.',
          createdAt: '2024-02-14T14:22:00Z',
          messages: [
            {
              id: 1,
              role: 'user',
              content: 'I need help creating assessment guidelines for technology competencies.',
              timestamp: '2024-02-14T14:22:00Z',
              tokens: 134
            }
          ]
        },
        {
          id: 3,
          title: 'Curriculum Development Help',
          user: { id: 3, name: 'Mike Johnson', email: 'mike@example.com' },
          model: 'claude-3',
          messageCount: 23,
          totalTokens: 5678,
          duration: 2567,
          lastMessage: 'This curriculum structure looks perfect for our needs.',
          createdAt: '2024-02-13T09:15:00Z',
          messages: []
        },
        {
          id: 4,
          title: 'Finance Competency Standards',
          user: { id: 4, name: 'Sarah Wilson', email: 'sarah@example.com' },
          model: 'gpt-4',
          messageCount: 12,
          totalTokens: 2876,
          duration: 1756,
          lastMessage: 'The finance competency standards are now clear to me.',
          createdAt: '2024-02-12T16:45:00Z',
          messages: []
        },
        {
          id: 5,
          title: 'Assessment Template Creation',
          user: { id: 5, name: 'David Brown', email: 'david@example.com' },
          model: 'gpt-3.5-turbo',
          messageCount: 19,
          totalTokens: 4123,
          duration: 2134,
          lastMessage: 'The template works perfectly for our assessment needs.',
          createdAt: '2024-02-11T11:30:00Z',
          messages: []
        }
      ]
    }

    const loadUsers = () => {
      // TODO: Replace with actual API call
      users.value = [
        { id: 1, name: 'John Doe' },
        { id: 2, name: 'Jane Smith' },
        { id: 3, name: 'Mike Johnson' },
        { id: 4, name: 'Sarah Wilson' },
        { id: 5, name: 'David Brown' }
      ]
    }

    const getModelClass = (model) => {
      const classes = {
        'gpt-4': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
        'gpt-3.5-turbo': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
        'claude-3': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300'
      }
      return classes[model] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }

    const formatTokens = (tokens) => {
      if (tokens >= 1000) {
        return (tokens / 1000).toFixed(1) + 'K'
      }
      return tokens.toString()
    }

    const formatDuration = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins}m ${secs}s`
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatTime = (dateString) => {
      return new Date(dateString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const selectAll = () => {
      if (selectedChats.value.length === filteredChats.value.length) {
        selectedChats.value = []
      } else {
        selectedChats.value = filteredChats.value.map(c => c.id)
      }
    }

    const toggleSelectAll = (event) => {
      if (event.target.checked) {
        selectedChats.value = filteredChats.value.map(c => c.id)
      } else {
        selectedChats.value = []
      }
    }

    const bulkExport = () => {
      // TODO: Implement bulk export
      console.log('Bulk export:', selectedChats.value)
      selectedChats.value = []
    }

    const bulkArchive = () => {
      // TODO: Implement bulk archive
      console.log('Bulk archive:', selectedChats.value)
      selectedChats.value = []
    }

    const bulkDelete = () => {
      if (confirm('Are you sure you want to delete the selected conversations?')) {
        // TODO: Implement bulk delete
        console.log('Bulk delete:', selectedChats.value)
        selectedChats.value = []
      }
    }

    const viewChat = (chat) => {
      selectedChat.value = chat
      showChatModal.value = true
    }

    const exportChat = (chat) => {
      // TODO: Implement chat export
      console.log('Export chat:', chat.id)
    }

    const deleteChat = (chat) => {
      if (confirm(`Are you sure you want to delete the conversation "${chat.title}"?`)) {
        const index = chats.value.findIndex(c => c.id === chat.id)
        if (index > -1) {
          chats.value.splice(index, 1)
        }
      }
    }

    const exportChatData = () => {
      // TODO: Implement data export
      console.log('Exporting chat data')
    }

    // Lifecycle
    onMounted(() => {
      loadChats()
      loadUsers()
    })

    return {
      // Data
      chats,
      users,
      selectedChats,
      searchQuery,
      selectedUser,
      selectedModel,
      dateRange,
      currentPage,
      itemsPerPage,
      chatStats,
      modelUsage,
      topUsers,
      tokenAnalysis,
      
      // Modals
      showChatModal,
      showAnalyticsModal,
      selectedChat,
      
      // Computed
      filteredChats,
      paginatedChats,
      totalPages,
      
      // Methods
      getModelClass,
      formatTokens,
      formatDuration,
      formatDate,
      formatTime,
      selectAll,
      toggleSelectAll,
      bulkExport,
      bulkArchive,
      bulkDelete,
      viewChat,
      exportChat,
      deleteChat,
      exportChatData
    }
  }
}
</script>
