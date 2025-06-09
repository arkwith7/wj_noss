<template>
  <nav class="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo and Navigation -->
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-sm">N</span>
              </div>
              <span class="text-xl font-bold text-gray-900 dark:text-white">NOSS</span>
            </router-link>
          </div>
          
          <!-- Desktop Navigation -->
          <div class="hidden md:ml-8 md:flex md:space-x-8">
            <template v-if="authStore.isAuthenticated">
              <router-link
                to="/home"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                :class="{ 'border-b-2 border-blue-500': $route.name === 'Home' }"
              >
                Home
              </router-link>
              <!-- <router-link
                to="/dashboard"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                :class="{ 'border-b-2 border-blue-500 text-gray-900 dark:text-white': $route.name === 'Dashboard' }"
              >
                Dashboard
              </router-link> -->
              <router-link
                to="/chat"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                :class="{ 'border-b-2 border-blue-500 text-gray-900 dark:text-white': $route.name === 'Chat' }"
              >
                Chat
              </router-link>
              <router-link
                to="/template-generation"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                :class="{ 'border-b-2 border-blue-500 text-gray-900 dark:text-white': $route.name === 'TemplateGeneration' }"
              >
                Templates
              </router-link>
              <router-link
                v-if="authStore.isAdmin"
                to="/admin"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                :class="{ 'border-b-2 border-blue-500 text-gray-900 dark:text-white': $route.path.startsWith('/admin') }"
              >
                Admin
              </router-link>
            </template>
          </div>
        </div>

        <!-- Right side -->
        <div class="flex items-center space-x-4">
          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg"
          >
            <svg v-if="appStore.theme === 'dark'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
            </svg>
          </button>

          <!-- User Menu -->
          <div v-if="authStore.isAuthenticated" class="relative" ref="userMenuRef">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center space-x-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg p-2"
            >
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">
                  {{ authStore.username.charAt(0).toUpperCase() }}
                </span>
              </div>
              <span>{{ authStore.username }}</span>
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- User Dropdown -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-show="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5 z-50"
              >
                <router-link
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click="showUserMenu = false"
                >
                  Profile
                </router-link>
                <router-link
                  to="/history"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  @click="showUserMenu = false"
                >
                  History
                </router-link>
                <div class="border-t border-gray-100 dark:border-gray-700"></div>
                <button
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  Sign out
                </button>
              </div>
            </transition>
          </div>

          <!-- Login/Register buttons -->
          <div v-else class="flex items-center space-x-3">
            <router-link
              to="/login"
              class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white px-3 py-2 text-sm font-medium"
            >
              Sign in
            </router-link>
            <router-link
              to="/register"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Sign up
            </router-link>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="appStore.toggleSidebar"
            class="md:hidden p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-show="appStore.sidebarOpen" class="md:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <template v-if="authStore.isAuthenticated">
          <router-link
            to="/home"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Home
          </router-link>
          <!-- <router-link
            to="/dashboard"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Dashboard
          </router-link> -->
          <router-link
            to="/chat"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Chat
          </router-link>
          <router-link
            to="/template-generation"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Templates
          </router-link>
          <router-link
            v-if="authStore.isAdmin"
            to="/admin"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Admin
          </router-link>
        </template>
        <template v-else>
          <router-link
            to="/login"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Sign in
          </router-link>
          <router-link
            to="/register"
            class="block px-3 py-2 text-base font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md"
            @click="appStore.closeSidebar"
          >
            Sign up
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useAppStore } from '../store'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

const showUserMenu = ref(false)
const userMenuRef = ref(null)

const toggleTheme = () => {
  const newTheme = appStore.theme === 'light' ? 'dark' : 'light'
  appStore.setTheme(newTheme)
}

const handleLogout = () => {
  authStore.logout()
  showUserMenu.value = false
  router.push('/')
}

const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
