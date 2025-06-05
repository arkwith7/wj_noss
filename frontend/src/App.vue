<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <!-- Global Loading Spinner -->
    <LoadingSpinner v-if="appStore.loading" />
    
    <!-- Navigation Bar -->
    <AppNavbar v-if="!isPublicRoute" />
    
    <!-- Main Content -->
    <main :class="{ 'pt-16': !isPublicRoute }">
      <router-view />
    </main>
    
    <!-- Footer for public pages -->
    <AppFooter v-if="isPublicRoute" />
    
    <!-- Notification System -->
    <NotificationSystem />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from './store/index.js'
import AppNavbar from './components/AppNavbar.vue'
import AppFooter from './components/AppFooter.vue'
import NotificationSystem from './components/NotificationSystem.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'

const route = useRoute()
const appStore = useAppStore()

// Determine if current route is public (landing, login, register)
const isPublicRoute = computed(() => {
  const publicRoutes = ['Landing', 'Login', 'Register']
  return publicRoutes.includes(route.name)
})

// Initialize theme on app startup
onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'light'
  appStore.setTheme(savedTheme)
})
</script>

<style>
/* Global styles */
#app {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background-color: rgb(243 244 246);
}

.dark ::-webkit-scrollbar-track {
  background-color: rgb(31 41 55);
}

::-webkit-scrollbar-thumb {
  background-color: rgb(209 213 219);
  border-radius: 9999px;
}

.dark ::-webkit-scrollbar-thumb {
  background-color: rgb(75 85 99);
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgb(156 163 175);
}

.dark ::-webkit-scrollbar-thumb:hover {
  background-color: rgb(107 114 128);
}

/* Ensure smooth transitions for theme changes */
* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
