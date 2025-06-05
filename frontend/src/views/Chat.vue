<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 h-[calc(100vh-12rem)]">
        <!-- Chat Sidebar -->
        <div class="lg:col-span-1 bg-white dark:bg-gray-800 rounded-lg shadow h-full flex flex-col">
          <!-- Header -->
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <h2 class="text-lg font-medium text-gray-900 dark:text-white">AI Assistant</h2>
              <button
                @click="startNewChat"
                class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
            </div>
          </div>

          <!-- AI Model Selection -->
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              AI Model
            </label>
            <select
              v-model="selectedModel"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="gpt-4">GPT-4 (Most Capable)</option>
              <option value="gpt-3.5">GPT-3.5 (Faster)</option>
              <option value="claude-3">Claude-3 (Alternative)</option>
            </select>
          </div>

          <!-- Chat History -->
          <div class="flex-1 overflow-y-auto">
            <div class="p-2">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2 px-2">Recent Chats</h3>
              <div class="space-y-1">
                <div
                  v-for="chat in chatHistory"
                  :key="chat.id"
                  @click="loadChat(chat)"
                  :class="[
                    'flex items-center p-2 rounded-lg cursor-pointer transition-colors',
                    currentChatId === chat.id
                      ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-900 dark:text-blue-100'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  ]"
                >
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate">{{ chat.title }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ chat.preview }}</p>
                  </div>
                  <button
                    @click.stop="deleteChat(chat)"
                    class="ml-2 p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Token Usage -->
          <div class="p-4 border-t border-gray-200 dark:border-gray-700">
            <div class="text-xs text-gray-500 dark:text-gray-400">
              <div class="flex justify-between mb-1">
                <span>Tokens Used Today</span>
                <span>{{ dailyTokens.used.toLocaleString() }} / {{ dailyTokens.limit.toLocaleString() }}</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1">
                <div 
                  class="bg-blue-600 h-1 rounded-full transition-all duration-300"
                  :style="{ width: `${Math.min((dailyTokens.used / dailyTokens.limit) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Chat Main Area -->
        <div class="lg:col-span-3 bg-white dark:bg-gray-800 rounded-lg shadow h-full flex flex-col">
          <!-- Chat Header -->
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                  {{ currentChat?.title || 'New Chat' }}
                </h1>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  AI-powered NOSS development assistant
                </p>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  @click="exportChat"
                  class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </button>
                <button
                  @click="clearChat"
                  class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Messages Area -->
          <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
            <!-- Welcome Message -->
            <div v-if="messages.length === 0" class="text-center py-12">
              <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Welcome to NOSS AI Assistant
              </h3>
              <p class="text-gray-500 dark:text-gray-400 mb-6">
                I can help you with NOSS development, curriculum design, and educational content creation.
              </p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                <button
                  v-for="suggestion in quickSuggestions"
                  :key="suggestion.id"
                  @click="sendMessage(suggestion.text)"
                  class="p-4 text-left border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                      <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ suggestion.title }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ suggestion.description }}</p>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Chat Messages -->
            <div
              v-for="message in messages"
              :key="message.id"
              :class="[
                'flex',
                message.role === 'user' ? 'justify-end' : 'justify-start'
              ]"
            >
              <div
                :class="[
                  'flex max-w-[80%] space-x-3',
                  message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                ]"
              >
                <!-- Avatar -->
                <div class="flex-shrink-0">
                  <div
                    :class="[
                      'w-8 h-8 rounded-full flex items-center justify-center',
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                    ]"
                  >
                    <svg v-if="message.role === 'user'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>

                <!-- Message Content -->
                <div
                  :class="[
                    'rounded-lg px-4 py-2',
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                  ]"
                >
                  <div class="text-sm whitespace-pre-wrap">{{ message.content }}</div>
                  <div class="text-xs mt-1 opacity-70">
                    {{ formatMessageTime(message.timestamp) }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Typing Indicator -->
            <div v-if="isTyping" class="flex justify-start">
              <div class="flex max-w-[80%] space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                    <svg class="w-4 h-4 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div class="bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2">
                  <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="p-4 border-t border-gray-200 dark:border-gray-700">
            <form @submit.prevent="sendUserMessage" class="flex space-x-2">
              <div class="flex-1 relative">
                <textarea
                  v-model="messageInput"
                  @keydown.enter.prevent="handleEnterKey"
                  :disabled="isTyping"
                  placeholder="Ask me about NOSS development, curriculum design, or educational standards..."
                  rows="1"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                  style="min-height: 48px; max-height: 120px;"
                ></textarea>
                <div class="absolute bottom-2 right-2 text-xs text-gray-400">
                  Press Enter to send, Shift+Enter for new line
                </div>
              </div>
              <button
                type="submit"
                :disabled="!messageInput.trim() || isTyping"
                class="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <svg v-if="isTyping" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useAppStore } from '../store'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

// Reactive data
const selectedModel = ref('gpt-4')
const messageInput = ref('')
const isTyping = ref(false)
const currentChatId = ref(null)
const messagesContainer = ref(null)

const messages = reactive([])
const chatHistory = reactive([
  {
    id: 1,
    title: 'NOSS Structure Discussion',
    preview: 'How to organize competency units...',
    createdAt: '2024-06-05T10:00:00Z'
  },
  {
    id: 2,
    title: 'Assessment Criteria Design',
    preview: 'Creating effective assessment methods...',
    createdAt: '2024-06-04T15:30:00Z'
  }
])

const dailyTokens = reactive({
  used: 15000,
  limit: 50000
})

const currentChat = computed(() => {
  return chatHistory.find(chat => chat.id === currentChatId.value)
})

const quickSuggestions = [
  {
    id: 1,
    title: 'Create NOSS Template',
    description: 'Generate a new NOSS template structure',
    text: 'Help me create a NOSS template for software development skills'
  },
  {
    id: 2,
    title: 'Assessment Design',
    description: 'Design assessment criteria and methods',
    text: 'How do I design effective assessment criteria for technical skills?'
  },
  {
    id: 3,
    title: 'Learning Outcomes',
    description: 'Define clear learning outcomes',
    text: 'Help me write clear and measurable learning outcomes for programming courses'
  },
  {
    id: 4,
    title: 'Competency Mapping',
    description: 'Map skills to industry standards',
    text: 'How do I map technical competencies to industry requirements?'
  }
]

// Methods
const sendUserMessage = async () => {
  if (!messageInput.value.trim() || isTyping.value) return

  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: messageInput.value,
    timestamp: new Date().toISOString()
  }

  messages.push(userMessage)
  messageInput.value = ''

  await scrollToBottom()
  await simulateAIResponse(userMessage.content)
}

const sendMessage = async (text) => {
  messageInput.value = text
  await sendUserMessage()
}

const simulateAIResponse = async (userMessage) => {
  isTyping.value = true
  await scrollToBottom()

  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))

  // Mock AI response based on user message
  let response = "I'd be happy to help you with that! "
  
  if (userMessage.toLowerCase().includes('noss') || userMessage.toLowerCase().includes('template')) {
    response += "NOSS (National Occupational Skills Standard) templates typically include competency units, performance criteria, knowledge and understanding requirements, and assessment guidelines. Would you like me to help you create a specific template for a particular field?"
  } else if (userMessage.toLowerCase().includes('assessment')) {
    response += "For effective assessment design, consider using a mix of practical demonstrations, written assessments, and portfolio-based evaluations. The key is to align assessment methods with the specific competencies being measured."
  } else if (userMessage.toLowerCase().includes('learning outcomes')) {
    response += "Clear learning outcomes should be specific, measurable, achievable, relevant, and time-bound (SMART). They should describe what learners will be able to do after completing the training."
  } else {
    response += "Could you provide more specific details about what you'd like to accomplish? I can assist with NOSS development, curriculum design, assessment creation, and more."
  }

  const aiMessage = {
    id: Date.now(),
    role: 'assistant',
    content: response,
    timestamp: new Date().toISOString()
  }

  messages.push(aiMessage)
  isTyping.value = false

  // Update daily token usage (mock)
  dailyTokens.used += Math.floor(Math.random() * 500) + 100

  await scrollToBottom()
}

const handleEnterKey = (event) => {
  if (event.shiftKey) {
    // Allow new line with Shift+Enter
    return
  }
  // Send message with Enter
  sendUserMessage()
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const startNewChat = () => {
  currentChatId.value = null
  messages.splice(0, messages.length)
  messageInput.value = ''
}

const loadChat = (chat) => {
  currentChatId.value = chat.id
  messages.splice(0, messages.length)
  // TODO: Load actual chat messages from API
  appStore.addNotification({
    type: 'info',
    title: 'Chat loaded',
    message: `Loaded chat: ${chat.title}`
  })
}

const deleteChat = (chat) => {
  if (confirm(`Delete chat "${chat.title}"?`)) {
    const index = chatHistory.findIndex(c => c.id === chat.id)
    if (index > -1) {
      chatHistory.splice(index, 1)
    }
    if (currentChatId.value === chat.id) {
      startNewChat()
    }
    appStore.addNotification({
      type: 'success',
      title: 'Chat deleted',
      message: `"${chat.title}" has been deleted`
    })
  }
}

const clearChat = () => {
  if (confirm('Clear current chat?')) {
    messages.splice(0, messages.length)
  }
}

const exportChat = () => {
  const chatData = {
    title: currentChat.value?.title || 'New Chat',
    messages: messages,
    model: selectedModel.value,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `chat-export-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
  
  appStore.addNotification({
    type: 'success',
    title: 'Chat exported',
    message: 'Chat has been downloaded as JSON file'
  })
}

const formatMessageTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Initialize
onMounted(() => {
  // Focus on input
  nextTick(() => {
    const input = document.querySelector('textarea')
    if (input) input.focus()
  })
})
</script>

<style scoped>
/* Custom scrollbar for messages area */
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

/* Auto-growing textarea */
textarea {
  resize: none;
  overflow-y: hidden;
}
</style>
