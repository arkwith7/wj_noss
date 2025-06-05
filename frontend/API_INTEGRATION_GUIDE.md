# API Integration Guide

This guide provides instructions for connecting the NOSS frontend to backend APIs.

## 🔌 Backend Integration Steps

### 1. Update API Base URL

Update the API service configuration:

```javascript
// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
```

### 2. Authentication Integration

Replace mock authentication in `src/store/auth.js`:

```javascript
// Example login action
const login = async (credentials) => {
  try {
    loading.value = true
    const response = await api.post('/auth/login', credentials)
    
    token.value = response.data.token
    user.value = response.data.user
    localStorage.setItem('auth_token', token.value)
    
    return { success: true }
  } catch (error) {
    return { 
      success: false, 
      message: error.response?.data?.message || 'Login failed' 
    }
  } finally {
    loading.value = false
  }
}
```

### 3. Dashboard API Integration

Update `Dashboard.vue` to fetch real data:

```javascript
// In Dashboard.vue setup function
const fetchDashboardData = async () => {
  try {
    const [statsRes, activityRes] = await Promise.all([
      api.get('/dashboard/statistics'),
      api.get('/dashboard/recent-activity')
    ])
    
    statistics.value = statsRes.data
    recentActivity.value = activityRes.data
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    // Handle error appropriately
  }
}

onMounted(() => {
  fetchDashboardData()
})
```

### 4. File Upload Integration

Connect upload functionality in relevant components:

```javascript
// Example upload function
const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const progress = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        // Update progress bar
      }
    })
    
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Upload failed')
  }
}
```

### 5. Chat Integration

Connect chat functionality with WebSocket or REST APIs:

```javascript
// In Chat.vue
const sendMessage = async (message) => {
  try {
    const response = await api.post('/chat/messages', {
      message: message,
      model: selectedModel.value
    })
    
    // Add message to chat
    messages.value.push({
      id: Date.now(),
      content: message,
      sender: 'user',
      timestamp: new Date()
    })
    
    // Add AI response
    messages.value.push({
      id: Date.now() + 1,
      content: response.data.response,
      sender: 'ai',
      timestamp: new Date()
    })
    
    // Update token usage
    tokenUsage.value.used += response.data.tokens_used
    
  } catch (error) {
    console.error('Failed to send message:', error)
  }
}
```

### 6. Admin API Integration

Connect admin management functions:

```javascript
// Example for UserManagement.vue
const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/users', {
      params: {
        search: searchQuery.value,
        role: selectedRole.value,
        status: selectedStatus.value,
        page: currentPage.value,
        limit: itemsPerPage.value
      }
    })
    
    users.value = response.data.users
    totalUsers.value = response.data.total
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

const createUser = async (userData) => {
  try {
    const response = await api.post('/admin/users', userData)
    users.value.push(response.data)
    showCreateUserModal.value = false
    
    // Show success notification
    appStore.addNotification({
      type: 'success',
      message: 'User created successfully'
    })
  } catch (error) {
    console.error('Failed to create user:', error)
    // Show error notification
  }
}
```

## 🔄 WebSocket Integration

For real-time features like chat and live updates:

```javascript
// src/services/websocket.js
class WebSocketService {
  constructor() {
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
  }
  
  connect() {
    const token = localStorage.getItem('auth_token')
    this.ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`)
    
    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
    }
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.handleMessage(data)
    }
    
    this.ws.onclose = () => {
      this.reconnect()
    }
  }
  
  handleMessage(data) {
    switch (data.type) {
      case 'chat_message':
        // Handle chat message
        break
      case 'system_update':
        // Handle system updates
        break
      case 'notification':
        // Handle notifications
        break
    }
  }
  
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    }
  }
  
  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.reconnectAttempts++
        this.connect()
      }, 1000 * this.reconnectAttempts)
    }
  }
}

export default new WebSocketService()
```

## 📋 API Endpoints Reference

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token

### Dashboard

- `GET /api/dashboard/statistics` - Get dashboard stats
- `GET /api/dashboard/recent-activity` - Get recent activity

### Documents

- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List documents
- `GET /api/documents/:id` - Get document details
- `DELETE /api/documents/:id` - Delete document

### Templates

- `GET /api/templates` - List templates
- `POST /api/templates/generate` - Generate template
- `GET /api/templates/:id` - Get template
- `PUT /api/templates/:id` - Update template

### Chat

- `POST /api/chat/messages` - Send chat message
- `GET /api/chat/history` - Get chat history
- `GET /api/chat/models` - Get available AI models

### Admin

- `GET /api/admin/users` - List users
- `POST /api/admin/users` - Create user
- `PUT /api/admin/users/:id` - Update user
- `DELETE /api/admin/users/:id` - Delete user
- `GET /api/admin/system/status` - System status
- `GET /api/admin/analytics` - Analytics data

## 🔒 Environment Variables

Create `.env` file in frontend root:

```bash
# API Configuration
VUE_APP_API_BASE_URL=http://localhost:8000/api
VUE_APP_WS_URL=ws://localhost:8000/ws

# Feature Flags
VUE_APP_ENABLE_CHAT=true
VUE_APP_ENABLE_ANALYTICS=true

# Debug
VUE_APP_DEBUG=true
```

## 🚨 Error Handling

Implement global error handling:

```javascript
// src/utils/errorHandler.js
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response
    
    switch (status) {
      case 401:
        // Redirect to login
        router.push('/login')
        break
      case 403:
        // Show permission denied message
        break
      case 500:
        // Show server error message
        break
      default:
        // Show generic error
    }
    
    return data.message || 'An error occurred'
  } else if (error.request) {
    // Network error
    return 'Network error. Please check your connection.'
  } else {
    // Other error
    return error.message || 'An unexpected error occurred'
  }
}
```

## 📚 Testing Integration

Example API testing with the frontend:

```javascript
// Example test for login functionality
describe('Authentication', () => {
  it('should login successfully', async () => {
    const credentials = {
      email: 'test@example.com',
      password: 'password123'
    }
    
    const response = await api.post('/auth/login', credentials)
    expect(response.data.token).toBeDefined()
    expect(response.data.user).toBeDefined()
  })
})
```

---

**Next Steps:**
1. Set up backend API endpoints
2. Update frontend API calls
3. Test integration thoroughly
4. Add error handling and loading states
5. Implement real-time features if needed
