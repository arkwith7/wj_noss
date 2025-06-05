import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const username = computed(() => user.value?.username || user.value?.email || '')

  // Actions
  const login = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      // JSON 방식 엔드포인트로 요청
      const response = await axios.post('/api/auth/login/json', {
        username: credentials.email, // email 입력값을 username으로 매핑
        password: credentials.password
      })
      const { access_token, user: userData } = response.data

      token.value = access_token
      user.value = userData
      localStorage.setItem('token', access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/auth/register', userData)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  const fetchUser = async () => {
    if (!token.value) return
    
    try {
      const response = await axios.get('/api/auth/me')
      user.value = response.data
    } catch (err) {
      console.error('Failed to fetch user:', err)
      logout()
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put('/api/auth/profile', profileData)
      user.value = { ...user.value, ...response.data }
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Profile update failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    loading.value = true
    error.value = null
    
    try {
      await axios.put('/api/auth/change-password', passwordData)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Password change failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Initialize auth header if token exists
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    fetchUser()
  }

  return {
    // State
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    isAdmin,
    username,
    
    // Actions
    login,
    register,
    logout,
    fetchUser,
    updateProfile,
    changePassword
  }
})
