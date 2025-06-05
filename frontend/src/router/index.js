import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

// Public pages
import Landing from '../views/Landing.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

// User pages  
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import Chat from '../views/Chat.vue'
import TemplateGeneration from '../views/TemplateGeneration.vue'
import History from '../views/History.vue'
import Profile from '../views/Profile.vue'

// Admin pages
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import DocumentManagement from '../views/admin/DocumentManagement.vue'
import TemplateManagement from '../views/admin/TemplateManagement.vue'
import MetadataManagement from '../views/admin/MetadataManagement.vue'
import ChatHistoryManagement from '../views/admin/ChatHistoryManagement.vue'
import TokenUsageManagement from '../views/admin/TokenUsageManagement.vue'
import UserManagement from '../views/admin/UserManagement.vue'

const routes = [
  // Public routes
  {
    path: '/',
    name: 'Landing',
    component: Landing,
    meta: { requiresGuest: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  
  // User routes
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    meta: { requiresAuth: true }
  },
  {
    path: '/template-generation',
    name: 'TemplateGeneration',
    component: TemplateGeneration,
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: History,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  
  // Admin routes
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/documents',
    name: 'DocumentManagement',
    component: DocumentManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/templates',
    name: 'TemplateManagement',
    component: TemplateManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/metadata',
    name: 'MetadataManagement',
    component: MetadataManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/chat-history',
    name: 'ChatHistoryManagement',
    component: ChatHistoryManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/token-usage',
    name: 'TokenUsageManagement',
    component: TokenUsageManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/home')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/home')
  } else {
    next()
  }
})

export default router
