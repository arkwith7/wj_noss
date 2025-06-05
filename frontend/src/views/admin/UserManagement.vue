<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">User Management</h1>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage user accounts, roles, and permissions</p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="showCreateUserModal = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <UserPlusIcon class="h-5 w-5" />
              <span>Add User</span>
            </button>
            <button
              @click="showImportModal = true"
              class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <ArrowUpTrayIcon class="h-5 w-5" />
              <span>Import Users</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="px-4 sm:px-6 lg:px-8 py-8">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <UsersIcon class="h-8 w-8 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Users</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ statistics.totalUsers }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CheckCircleIcon class="h-8 w-8 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Active Users</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ statistics.activeUsers }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <UserGroupIcon class="h-8 w-8 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Admins</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ statistics.adminUsers }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ClockIcon class="h-8 w-8 text-orange-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">New This Month</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ statistics.newThisMonth }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-3">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
            <!-- Filters and Search -->
            <div class="p-6 border-b border-gray-200 dark:border-gray-700">
              <div class="flex flex-col sm:flex-row gap-4">
                <div class="flex-1">
                  <div class="relative">
                    <MagnifyingGlassIcon class="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Search users..."
                      class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                </div>
                <select
                  v-model="selectedRole"
                  class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  <option value="">All Roles</option>
                  <option value="admin">Admin</option>
                  <option value="user">User</option>
                  <option value="guest">Guest</option>
                </select>
                <select
                  v-model="selectedStatus"
                  class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>

              <!-- Bulk Actions -->
              <div v-if="selectedUsers.length > 0" class="mt-4 flex items-center justify-between bg-blue-50 dark:bg-blue-900 p-3 rounded-lg">
                <span class="text-sm font-medium text-blue-800 dark:text-blue-200">
                  {{ selectedUsers.length }} user(s) selected
                </span>
                <div class="flex space-x-2">
                  <button
                    @click="bulkAction('activate')"
                    class="text-green-600 hover:text-green-800 text-sm font-medium"
                  >
                    Activate
                  </button>
                  <button
                    @click="bulkAction('suspend')"
                    class="text-orange-600 hover:text-orange-800 text-sm font-medium"
                  >
                    Suspend
                  </button>
                  <button
                    @click="bulkAction('delete')"
                    class="text-red-600 hover:text-red-800 text-sm font-medium"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>

            <!-- Users Table -->
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="px-6 py-3 text-left">
                      <input
                        type="checkbox"
                        @change="toggleAllUsers"
                        :checked="selectedUsers.length === filteredUsers.length && filteredUsers.length > 0"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      User
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Role
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Status
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Last Active
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="user in paginatedUsers" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td class="px-6 py-4">
                      <input
                        type="checkbox"
                        :value="user.id"
                        v-model="selectedUsers"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                          <img :src="user.avatar" :alt="user.name" class="h-10 w-10 rounded-full" />
                        </div>
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900 dark:text-white">{{ user.name }}</div>
                          <div class="text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="getRoleBadgeClass(user.role)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                        {{ user.role }}
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="getStatusBadgeClass(user.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                        {{ user.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {{ formatDate(user.lastActive) }}
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex space-x-2">
                        <button
                          @click="editUser(user)"
                          class="text-blue-600 hover:text-blue-800 dark:text-blue-400"
                          title="Edit User"
                        >
                          <PencilIcon class="h-5 w-5" />
                        </button>
                        <button
                          @click="viewUserDetails(user)"
                          class="text-gray-600 hover:text-gray-800 dark:text-gray-400"
                          title="View Details"
                        >
                          <EyeIcon class="h-5 w-5" />
                        </button>
                        <button
                          @click="deleteUser(user)"
                          class="text-red-600 hover:text-red-800 dark:text-red-400"
                          title="Delete User"
                        >
                          <TrashIcon class="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination -->
            <div class="bg-white dark:bg-gray-800 px-4 py-3 border-t border-gray-200 dark:border-gray-700 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex justify-between flex-1 sm:hidden">
                  <button
                    @click="previousPage"
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
                  >
                    Previous
                  </button>
                  <button
                    @click="nextPage"
                    :disabled="currentPage === totalPages"
                    class="relative ml-3 inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
                  >
                    Next
                  </button>
                </div>
                <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                  <div>
                    <p class="text-sm text-gray-700 dark:text-gray-300">
                      Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} of {{ filteredUsers.length }} results
                    </p>
                  </div>
                  <div class="flex space-x-1">
                    <button
                      v-for="page in visiblePages"
                      :key="page"
                      @click="goToPage(page)"
                      :class="page === currentPage ? 'bg-blue-600 text-white' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'"
                      class="px-3 py-1 rounded-md text-sm font-medium"
                    >
                      {{ page }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h3>
            <div class="space-y-3">
              <button
                @click="showCreateUserModal = true"
                class="w-full text-left px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900 rounded-lg"
              >
                <UserPlusIcon class="h-4 w-4 inline mr-2" />
                Add New User
              </button>
              <button
                @click="showImportModal = true"
                class="w-full text-left px-3 py-2 text-sm text-green-600 hover:bg-green-50 dark:hover:bg-green-900 rounded-lg"
              >
                <ArrowUpTrayIcon class="h-4 w-4 inline mr-2" />
                Import Users
              </button>
              <button
                @click="exportUsers"
                class="w-full text-left px-3 py-2 text-sm text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900 rounded-lg"
              >
                <ArrowDownTrayIcon class="h-4 w-4 inline mr-2" />
                Export Users
              </button>
              <button
                @click="showAuditLogModal = true"
                class="w-full text-left px-3 py-2 text-sm text-orange-600 hover:bg-orange-50 dark:hover:bg-orange-900 rounded-lg"
              >
                <DocumentTextIcon class="h-4 w-4 inline mr-2" />
                View Audit Log
              </button>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent User Activity</h3>
            <div class="space-y-3">
              <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
                <div :class="getActivityIcon(activity.type)" class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center">
                  <component :is="getActivityIconComponent(activity.type)" class="h-4 w-4 text-white" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-gray-900 dark:text-white">{{ activity.description }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(activity.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <div v-if="showCreateUserModal || showEditUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md m-4">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ showEditUserModal ? 'Edit User' : 'Create New User' }}
          </h3>
        </div>
        <form @submit.prevent="saveUser" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
            <input
              v-model="userForm.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input
              v-model="userForm.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
            <select
              v-model="userForm.role"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="user">User</option>
              <option value="admin">Admin</option>
              <option value="guest">Guest</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
            <select
              v-model="userForm.status"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="suspended">Suspended</option>
            </select>
          </div>
          <div v-if="!showEditUserModal">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
            <input
              v-model="userForm.password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            />
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeUserModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
            >
              {{ showEditUserModal ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- User Details Modal -->
    <div v-if="showUserDetailsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl m-4">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">User Details</h3>
        </div>
        <div v-if="selectedUser" class="p-6">
          <div class="flex items-center mb-6">
            <img :src="selectedUser.avatar" :alt="selectedUser.name" class="h-16 w-16 rounded-full" />
            <div class="ml-4">
              <h4 class="text-xl font-semibold text-gray-900 dark:text-white">{{ selectedUser.name }}</h4>
              <p class="text-gray-500 dark:text-gray-400">{{ selectedUser.email }}</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 mb-6">
            <div>
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400">Role</label>
              <p class="mt-1 text-sm text-gray-900 dark:text-white">{{ selectedUser.role }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400">Status</label>
              <p class="mt-1 text-sm text-gray-900 dark:text-white">{{ selectedUser.status }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400">Created</label>
              <p class="mt-1 text-sm text-gray-900 dark:text-white">{{ formatDate(selectedUser.createdAt) }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400">Last Active</label>
              <p class="mt-1 text-sm text-gray-900 dark:text-white">{{ formatDate(selectedUser.lastActive) }}</p>
            </div>
          </div>
          <div class="mb-6">
            <h5 class="text-lg font-medium text-gray-900 dark:text-white mb-3">Activity Summary</h5>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center">
                <p class="text-2xl font-semibold text-blue-600">{{ selectedUser.documentsProcessed || 0 }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">Documents</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-semibold text-green-600">{{ selectedUser.templatesGenerated || 0 }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">Templates</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-semibold text-purple-600">{{ selectedUser.aiChats || 0 }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">AI Chats</p>
              </div>
            </div>
          </div>
          <div class="flex justify-end">
            <button
              @click="showUserDetailsModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Import Users Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md m-4">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Import Users</h3>
        </div>
        <div class="p-6">
          <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center">
            <ArrowUpTrayIcon class="mx-auto h-12 w-12 text-gray-400" />
            <div class="mt-4">
              <label for="file-upload" class="cursor-pointer">
                <span class="mt-2 block text-sm font-medium text-gray-900 dark:text-white">
                  Upload CSV file
                </span>
                <input id="file-upload" name="file-upload" type="file" accept=".csv" class="sr-only" />
              </label>
              <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
                CSV should contain: name, email, role, status columns
              </p>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button
              @click="showImportModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg"
            >
              Cancel
            </button>
            <button
              @click="importUsers"
              class="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg"
            >
              Import
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Audit Log Modal -->
    <div v-if="showAuditLogModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-4xl m-4 max-h-[80vh] overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">User Management Audit Log</h3>
        </div>
        <div class="p-6 overflow-auto max-h-96">
          <div class="space-y-3">
            <div v-for="log in auditLogs" :key="log.id" class="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div :class="getActivityIcon(log.action)" class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center">
                <component :is="getActivityIconComponent(log.action)" class="h-4 w-4 text-white" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-900 dark:text-white">{{ log.description }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ log.admin }} • {{ formatDate(log.timestamp) }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex justify-end">
            <button
              @click="showAuditLogModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  UsersIcon, UserPlusIcon, UserGroupIcon, CheckCircleIcon, ClockIcon,
  MagnifyingGlassIcon, PencilIcon, EyeIcon, TrashIcon, ArrowUpTrayIcon,
  ArrowDownTrayIcon, DocumentTextIcon
} from '@heroicons/vue/24/outline'

// Reactive data
const searchQuery = ref('')
const selectedRole = ref('')
const selectedStatus = ref('')
const selectedUsers = ref([])
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Modal states
const showCreateUserModal = ref(false)
const showEditUserModal = ref(false)
const showUserDetailsModal = ref(false)
const showImportModal = ref(false)
const showAuditLogModal = ref(false)

// Form data
const userForm = ref({
  name: '',
  email: '',
  role: 'user',
  status: 'active',
  password: ''
})

const selectedUser = ref(null)

// Mock data - TODO: Replace with actual API calls
const statistics = ref({
  totalUsers: 1247,
  activeUsers: 1089,
  adminUsers: 12,
  newThisMonth: 43
})

const users = ref([
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@example.com',
    role: 'admin',
    status: 'active',
    avatar: 'https://ui-avatars.com/api/?name=John+Doe&background=3b82f6&color=fff',
    lastActive: new Date('2024-06-05T10:30:00'),
    createdAt: new Date('2024-01-15T09:00:00'),
    documentsProcessed: 245,
    templatesGenerated: 18,
    aiChats: 156
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    role: 'user',
    status: 'active',
    avatar: 'https://ui-avatars.com/api/?name=Jane+Smith&background=10b981&color=fff',
    lastActive: new Date('2024-06-05T11:15:00'),
    createdAt: new Date('2024-02-20T14:30:00'),
    documentsProcessed: 89,
    templatesGenerated: 7,
    aiChats: 234
  },
  {
    id: 3,
    name: 'Mike Johnson',
    email: 'mike.johnson@example.com',
    role: 'user',
    status: 'inactive',
    avatar: 'https://ui-avatars.com/api/?name=Mike+Johnson&background=f59e0b&color=fff',
    lastActive: new Date('2024-05-28T16:45:00'),
    createdAt: new Date('2024-03-10T11:00:00'),
    documentsProcessed: 12,
    templatesGenerated: 3,
    aiChats: 45
  },
  {
    id: 4,
    name: 'Sarah Wilson',
    email: 'sarah.wilson@example.com',
    role: 'admin',
    status: 'active',
    avatar: 'https://ui-avatars.com/api/?name=Sarah+Wilson&background=8b5cf6&color=fff',
    lastActive: new Date('2024-06-05T09:20:00'),
    createdAt: new Date('2024-01-08T10:30:00'),
    documentsProcessed: 567,
    templatesGenerated: 34,
    aiChats: 278
  },
  {
    id: 5,
    name: 'Robert Brown',
    email: 'robert.brown@example.com',
    role: 'user',
    status: 'suspended',
    avatar: 'https://ui-avatars.com/api/?name=Robert+Brown&background=ef4444&color=fff',
    lastActive: new Date('2024-05-20T13:10:00'),
    createdAt: new Date('2024-04-05T15:45:00'),
    documentsProcessed: 34,
    templatesGenerated: 2,
    aiChats: 67
  }
])

const recentActivity = ref([
  {
    id: 1,
    type: 'user_created',
    description: 'New user Alice Cooper registered',
    timestamp: new Date('2024-06-05T11:30:00')
  },
  {
    id: 2,
    type: 'user_suspended',
    description: 'User Robert Brown was suspended',
    timestamp: new Date('2024-06-05T10:15:00')
  },
  {
    id: 3,
    type: 'role_changed',
    description: 'User permissions updated for Jane Smith',
    timestamp: new Date('2024-06-05T09:45:00')
  }
])

const auditLogs = ref([
  {
    id: 1,
    action: 'user_created',
    description: 'Created new user account for Alice Cooper',
    admin: 'John Doe',
    timestamp: new Date('2024-06-05T11:30:00')
  },
  {
    id: 2,
    action: 'user_suspended',
    description: 'Suspended user account for Robert Brown due to policy violation',
    admin: 'Sarah Wilson',
    timestamp: new Date('2024-06-05T10:15:00')
  },
  {
    id: 3,
    action: 'role_changed',
    description: 'Changed user role from guest to user for Jane Smith',
    admin: 'John Doe',
    timestamp: new Date('2024-06-05T09:45:00')
  }
])

// Computed properties
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = !selectedRole.value || user.role === selectedRole.value
    const matchesStatus = !selectedStatus.value || user.status === selectedStatus.value
    
    return matchesSearch && matchesRole && matchesStatus
  })
})

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredUsers.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredUsers.value.length / itemsPerPage.value)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const getRoleBadgeClass = (role) => {
  const classes = {
    admin: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    user: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    guest: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
  }
  return classes[role] || classes.user
}

const getStatusBadgeClass = (status) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    inactive: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    suspended: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return classes[status] || classes.active
}

const getActivityIcon = (type) => {
  const classes = {
    user_created: 'bg-green-500',
    user_suspended: 'bg-red-500',
    role_changed: 'bg-blue-500',
    user_deleted: 'bg-red-600'
  }
  return classes[type] || 'bg-gray-500'
}

const getActivityIconComponent = (type) => {
  const components = {
    user_created: UserPlusIcon,
    user_suspended: TrashIcon,
    role_changed: PencilIcon,
    user_deleted: TrashIcon
  }
  return components[type] || DocumentTextIcon
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date))
}

const toggleAllUsers = () => {
  if (selectedUsers.value.length === filteredUsers.value.length) {
    selectedUsers.value = []
  } else {
    selectedUsers.value = filteredUsers.value.map(user => user.id)
  }
}

const bulkAction = (action) => {
  // TODO: Implement bulk actions
  console.log(`Bulk ${action} for users:`, selectedUsers.value)
  selectedUsers.value = []
}

const editUser = (user) => {
  selectedUser.value = user
  userForm.value = {
    name: user.name,
    email: user.email,
    role: user.role,
    status: user.status,
    password: ''
  }
  showEditUserModal.value = true
}

const viewUserDetails = (user) => {
  selectedUser.value = user
  showUserDetailsModal.value = true
}

const deleteUser = (user) => {
  if (confirm(`Are you sure you want to delete ${user.name}?`)) {
    // TODO: Implement user deletion
    console.log('Delete user:', user.id)
  }
}

const saveUser = () => {
  // TODO: Implement user save/update
  console.log('Save user:', userForm.value)
  closeUserModal()
}

const closeUserModal = () => {
  showCreateUserModal.value = false
  showEditUserModal.value = false
  selectedUser.value = null
  userForm.value = {
    name: '',
    email: '',
    role: 'user',
    status: 'active',
    password: ''
  }
}

const importUsers = () => {
  // TODO: Implement user import
  console.log('Import users')
  showImportModal.value = false
}

const exportUsers = () => {
  // TODO: Implement user export
  console.log('Export users')
}

// Pagination methods
const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page) => {
  currentPage.value = page
}

// Lifecycle
onMounted(() => {
  // TODO: Load users data from API
  console.log('UserManagement component mounted')
})
</script>
