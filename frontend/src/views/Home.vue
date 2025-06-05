<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Welcome Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              NOSS 교육과정 자동 생성 시스템
            </h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              AI 기반 국가직무능력표준 문서 처리 및 교육과정 생성 플랫폼
            </p>
          </div>
          <div class="flex space-x-3">
            <router-link
              to="/chat"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              AI 어시스턴트
            </router-link>
            <router-link
              to="/template-generation" 
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
            >
              <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              템플릿 생성
            </router-link>
          </div>
        </div>
      </div>

      <!-- System Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">등록된 문서</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.totalDocuments }}</p>
            </div>
          </div>
          <div class="mt-4">
            <div class="flex items-center text-sm text-green-600 dark:text-green-400">
              <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              이번 주 +{{ stats.weeklyGrowth }}개
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">처리 완료</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.processedDocuments }}</p>
            </div>
          </div>
          <div class="mt-4">
            <div class="flex items-center text-sm text-blue-600 dark:text-blue-400">
              <span>성공률 {{ stats.successRate }}%</span>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">생성된 템플릿</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.generatedTemplates }}</p>
            </div>
          </div>
          <div class="mt-4">
            <div class="flex items-center text-sm text-purple-600 dark:text-purple-400">
              <span>오늘 +{{ stats.todayTemplates }}개</span>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-orange-100 dark:bg-orange-900/50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">벡터 임베딩</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.vectorEmbeddings }}</p>
            </div>
          </div>
          <div class="mt-4">
            <div class="flex items-center text-sm text-orange-600 dark:text-orange-400">
              <span>검색 준비완료</span>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content Area -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Document Management Section -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 class="text-lg font-medium text-gray-900 dark:text-white">문서 관리 및 업로드</h2>
            </div>
            <div class="p-6">
              <!-- Document Type Tabs -->
              <div class="flex space-x-1 mb-6">
                <button
                  v-for="type in documentTypes"
                  :key="type.id"
                  @click="activeDocumentType = type.id"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    activeDocumentType === type.id
                      ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300'
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  ]"
                >
                  {{ type.name }} ({{ type.count }})
                </button>
              </div>

              <!-- File Upload Area -->
              <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 mb-6">
                <div class="text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <h3 class="mt-2 text-lg font-medium text-gray-900 dark:text-white">문서 업로드</h3>
                  <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    NOSS PDF, Excel 분류, Word 템플릿 파일을 업로드하세요. (최대 50MB)
                  </p>
                  <input
                    type="file"
                    ref="fileInput"
                    @change="handleFileChange"
                    class="mt-4 block w-full text-sm text-gray-500 dark:text-gray-400
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-full file:border-0
                           file:text-sm file:font-semibold
                           file:bg-blue-50 dark:file:bg-blue-900/50 file:text-blue-700 dark:file:text-blue-300
                           hover:file:bg-blue-100 dark:hover:file:bg-blue-800/50"
                  />
                </div>

                <div v-if="uploadError" class="mt-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 rounded-md">
                  <p class="text-sm">{{ uploadError }}</p>
                </div>

                <div v-if="selectedFile" class="mt-4">
                  <p class="text-sm text-gray-700 dark:text-gray-300">선택된 파일: {{ selectedFile.name }} ({{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB)</p>
                </div>

                <div v-if="isUploading" class="mt-4">
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-out" :style="{ width: uploadProgress + '%' }"></div>
                  </div>
                  <p class="text-sm text-blue-600 dark:text-blue-400 mt-1">{{ uploadProgress.toFixed(0) }}% 업로드 중...</p>
                </div>
                
                <button
                  @click="uploadFile"
                  :disabled="!selectedFile || isUploading"
                  class="mt-6 w-full inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg v-if="isUploading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isUploading ? '업로드 중...' : '선택 파일 업로드' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Processing Status (WebSocket) -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg mt-8">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-medium text-gray-900 dark:text-white">실시간 처리 상태</h2>
                <span :class="['px-2 py-0.5 rounded-full text-xs font-medium', websocketStatus === 'connected' ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300' : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300']">
                  {{ websocketStatus === 'connected' ? '연결됨' : '연결 끊김' }}
                </span>
              </div>
            </div>
            <div class="p-6 min-h-[150px] max-h-[300px] overflow-y-auto bg-gray-50 dark:bg-gray-800/50 rounded-b-lg">
              <div v-if="!processingStatus.length && websocketStatus === 'connected'" class="text-center text-gray-500 dark:text-gray-400 pt-10">
                처리 대기 중...
              </div>
              <div v-if="websocketStatus !== 'connected'" class="text-center text-red-500 dark:text-red-400 pt-10">
                WebSocket 연결이 끊어졌습니다. 자동 재연결 시도 중...
              </div>
              <ul v-if="processingStatus.length" class="space-y-2">
                <li v-for="(status, index) in processingStatus" :key="index" 
                    class="text-sm p-2 rounded-md"
                    :class="{
                      'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300': status.type === 'info',
                      'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300': status.type === 'success',
                      'bg-yellow-50 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300': status.type === 'warning',
                      'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300': status.type === 'error',
                    }">
                  <span class="font-medium">[{{ new Date(status.timestamp).toLocaleTimeString() }}]</span> {{ status.message }}
                  <div v-if="status.details" class="mt-1 text-xs pl-4">{{ status.details }}</div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Document Search Section -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg mt-8">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 class="text-lg font-medium text-gray-900 dark:text-white">문서 통합 검색</h2>
            </div>
            <div class="p-6">
              <div class="flex space-x-2 mb-4">
                <input 
                  type="text" 
                  v-model="searchQuery"
                  @keyup.enter="handleSearch"
                  placeholder="검색어를 입력하세요 (예: '인공지능 교육과정')"
                  class="flex-grow px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
                />
                <button
                  @click="handleSearch"
                  :disabled="isSearching || !searchQuery.trim()"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg v-if="isSearching" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isSearching ? '검색 중...' : '검색' }}
                </button>
              </div>

              <div v-if="searchError" class="mb-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 rounded-md">
                <p class="text-sm">{{ searchError }}</p>
              </div>
              
              <div v-if="isSearching && !searchResults.length" class="text-center py-8">
                <svg class="animate-spin mx-auto h-8 w-8 text-purple-600 dark:text-purple-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">검색 결과를 불러오는 중입니다...</p>
              </div>

              <div v-if="!isSearching && searchAttempted && !searchResults.length" class="text-center py-8 text-gray-500 dark:text-gray-400">
                검색 결과가 없습니다. 다른 검색어를 시도해보세요.
              </div>

              <div v-if="searchResults.length > 0" class="space-y-4">
                <div v-for="result in searchResults" :key="result.id" class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg shadow">
                  <h4 class="text-md font-semibold text-blue-600 dark:text-blue-400 hover:underline cursor-pointer" @click="viewDocument(result.id)">
                    {{ result.title || '제목 없음' }}
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1 clamp-lines-2" v-html="highlightMatches(result.snippet, searchQuery)"></p>
                  <div class="mt-2 text-xs text-gray-500 dark:text-gray-500">
                    <span>유형: {{ result.type || 'N/A' }}</span> | 
                    <span>관련도: {{ result.score ? result.score.toFixed(2) : 'N/A' }}</span> |
                    <span>수정일: {{ result.lastModified ? new Date(result.lastModified).toLocaleDateString() : 'N/A' }}</span>
                  </div>
                </div>
                 <button 
                    v-if="hasMoreSearchResults"
                    @click="loadMoreSearchResults" 
                    :disabled="isLoadingMore"
                    class="mt-4 w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50">
                    {{ isLoadingMore ? '더 불러오는 중...' : '더 보기' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Recent Documents -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-medium text-gray-900 dark:text-white">최근 문서</h2>
                <router-link to="/documents" class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
                  전체 보기
                </router-link>
              </div>
            </div>
            <div class="p-6">
              <FileList />
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Quick Actions -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">빠른 작업</h3>
            </div>
            <div class="p-6 space-y-3">
              <button
                @click="uploadDocument('noss_pdf')"
                class="w-full flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg class="mr-3 h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                NOSS PDF 업로드
                <span class="ml-auto text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">주요</span>
              </button>
              <button
                @click="uploadDocument('excel_classification')"
                class="w-full flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg class="mr-3 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                엑셀 분류 파일 업로드
                <span class="ml-auto text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">필수</span>
              </button>
              <button
                @click="uploadDocument('word_template')"
                class="w-full flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg class="mr-3 h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                워드 템플릿 업로드
                <span class="ml-auto text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">선택</span>
              </button>
              <router-link
                to="/template-generation"
                class="w-full flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg class="mr-3 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                새 템플릿 생성
              </router-link>
              <router-link
                to="/chat"
                class="w-full flex items-center px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg class="mr-3 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                AI 어시스턴트 상담
              </router-link>
            </div>
          </div>

          <!-- NOSS Classification Preview -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">NOSS 분류체계</h3>
            </div>
            <div class="p-6">
              <div class="space-y-3">
                <div v-for="category in nossCategories" :key="category.id" class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div :class="category.color" class="w-3 h-3 rounded-full mr-3"></div>
                    <span class="text-sm text-gray-900 dark:text-white">{{ category.name }}</span>
                  </div>
                  <span class="text-sm text-gray-500 dark:text-gray-400">{{ category.count }}</span>
                </div>
              </div>
              <div class="mt-4">
                <router-link to="/classification" class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
                  전체 분류 보기 →
                </router-link>
              </div>
            </div>
          </div>

          <!-- Vector Store Status -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">벡터 스토어 상태</h3>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">임베딩 완료</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ vectorStats.embedded }}/{{ vectorStats.total }}</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-green-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${(vectorStats.embedded / vectorStats.total) * 100}%` }"
                  ></div>
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  검색 성능: {{ vectorStats.searchPerformance }}ms 평균 응답시간
                </div>
              </div>
            </div>
          </div>

          <!-- Recent System Activity -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">시스템 활동</h3>
            </div>
            <div class="p-6">
              <div class="space-y-3">
                <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start space-x-3">
                  <div :class="activity.iconColor" class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center">
                    <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20" v-html="activity.icon"></svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm text-gray-900 dark:text-white">{{ activity.description }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">{{ activity.time }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import FileUpload from '../components/FileUpload.vue'
import ProcessStatus from '../components/ProcessStatus.vue'
import FileList from '../components/FileList.vue'
import { useAppStore } from '../store'
import axios from 'axios'

const router = useRouter()
const appStore = useAppStore()

// Reactive data
const activeDocumentType = ref('noss_pdf')

// 통계 데이터
const stats = reactive({
  totalDocuments: 0,
  processedDocuments: 0,
  generatedTemplates: 0,
  vectorEmbeddings: 0,
  weeklyGrowth: 0,
  successRate: 0,
  todayTemplates: 0,
})

// 문서 타입별 분류
const documentTypes = ref([
  { id: 'noss_pdf', name: 'NOSS PDF', count: 0 },
  { id: 'excel_classification', name: '엑셀 분류', count: 0 },
  { id: 'word_template', name: '워드 템플릿', count: 0 },
])

// NOSS 분류체계
const nossCategories = [
  { id: 1, name: '정보통신', count: 0, color: 'bg-blue-500' },
  { id: 2, name: '보건의료', count: 0, color: 'bg-green-500' },
  { id: 3, name: '제조업', count: 0, color: 'bg-purple-500' },
  { id: 4, name: '교육서비스', count: 0, color: 'bg-orange-500' },
  { id: 5, name: '금융보험', count: 0, color: 'bg-red-500' },
  { id: 6, name: '기타', count: 0, color: 'bg-gray-500' }
]

// 벡터 스토어 상태
const vectorStats = reactive({
  embedded: 0,
  total: 0,
  searchPerformance: 0
})

// 최근 시스템 활동
const recentActivities = [
  {
    id: 1,
    description: '새로운 NOSS PDF 문서가 처리되었습니다',
    time: '2분 전',
    icon: '<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
    iconColor: 'bg-green-500'
  },
  {
    id: 2,
    description: '교육과정 템플릿이 생성되었습니다',
    time: '5분 전',
    icon: '<path d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>',
    iconColor: 'bg-blue-500'
  },
  {
    id: 3,
    description: '벡터 임베딩이 완료되었습니다',
    time: '10분 전',
    icon: '<path d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>',
    iconColor: 'bg-purple-500'
  },
  {
    id: 4,
    description: 'AI 분석이 시작되었습니다',
    time: '15분 전',
    icon: '<path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>',
    iconColor: 'bg-orange-500'
  }
]

// 파일 업로드 관련
const fileInput = ref(null)
const selectedFile = ref(null)
const uploadProgress = ref(0)
const uploadError = ref('')
const isUploading = ref(false)
const MAX_FILE_SIZE = 50 * 1024 * 1024 // 50MB
const ALLOWED_FILE_TYPES = ['application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) {
    selectedFile.value = null
    uploadError.value = ''
    return
  }

  // 파일 크기 검증
  if (file.size > MAX_FILE_SIZE) {
    uploadError.value = `파일 크기가 너무 큽니다. 최대 ${MAX_FILE_SIZE / 1024 / 1024}MB까지 업로드 가능합니다.`
    selectedFile.value = null
    if (fileInput.value) fileInput.value.value = '' // 파일 입력 초기화
    return
  }

  // 파일 형식 검증
  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    uploadError.value = '지원하지 않는 파일 형식입니다. PDF, Excel, Word 파일을 업로드해주세요.'
    selectedFile.value = null
    if (fileInput.value) fileInput.value.value = '' // 파일 입력 초기화
    return
  }
  
  selectedFile.value = file
  uploadError.value = ''
  uploadProgress.value = 0
}

const uploadFile = async () => {
  if (!selectedFile.value || isUploading.value) return

  isUploading.value = true
  uploadProgress.value = 0
  uploadError.value = ''

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  // formData.append('documentType', activeDocumentType.value) // 필요시 문서 타입 정보 추가

  try {
    // 실제 API 엔드포인트로 교체해야 합니다.
    const response = await axios.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
      },
    })
    
    appStore.showNotification({ message: '파일이 성공적으로 업로드되었습니다.', type: 'success' })
    console.log('Upload successful:', response.data)
    selectedFile.value = null
    if (fileInput.value) fileInput.value.value = '' // 파일 입력 초기화
    // 업로드 성공 후 문서 목록 갱신 등의 로직 추가
    fetchStats() // 예시: 통계 업데이트
  } catch (error) {
    console.error('Upload failed:', error)
    uploadError.value = error.response?.data?.message || error.message || '파일 업로드 중 오류가 발생했습니다.'
    appStore.showNotification({ message: `파일 업로드 실패: ${uploadError.value}`, type: 'error' })
  } finally {
    isUploading.value = false
    uploadProgress.value = 0 // 완료 후 0으로 초기화하거나 100으로 유지 선택
  }
}

// WebSocket 관련
const socket = ref(null)
const processingStatus = ref([]) // { timestamp: Date, message: string, type: 'info'|'success'|'error'|'warning', details?: string }[]
const websocketStatus = ref('disconnected') // 'connected', 'disconnected', 'connecting'
let reconnectAttempts = 0
const MAX_RECONNECT_ATTEMPTS = 5

const connectWebSocket = () => {
  // 실제 WebSocket 서버 URL로 교체해야 합니다.
  const wsUrl = `ws://${window.location.host}/ws/status` 
  websocketStatus.value = 'connecting'
  
  socket.value = new WebSocket(wsUrl)

  socket.value.onopen = () => {
    console.log('WebSocket connected')
    websocketStatus.value = 'connected'
    appStore.showNotification({ message: '실시간 처리 상태 서버에 연결되었습니다.', type: 'info' })
    reconnectAttempts = 0 // 연결 성공 시 재시도 횟수 초기화
  }

  socket.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      console.log('WebSocket message received:', data)
      processingStatus.value.unshift({ // 최신 메시지를 맨 위에 추가
        timestamp: data.timestamp || new Date(),
        message: data.message,
        type: data.type || 'info',
        details: data.details
      })
      // 최대 메시지 개수 제한 (예: 100개)
      if (processingStatus.value.length > 100) {
        processingStatus.value.pop()
      }
    } catch (e) {
      console.error('Error parsing WebSocket message:', e)
      processingStatus.value.unshift({ timestamp: new Date(), message: event.data, type: 'info' })
    }
  }

  socket.value.onclose = (event) => {
    console.log('WebSocket disconnected:', event.code, event.reason)
    websocketStatus.value = 'disconnected'
    appStore.showNotification({ message: '실시간 처리 상태 서버와 연결이 끊어졌습니다.', type: 'warning' })
    
    // 재연결 로직
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      reconnectAttempts++
      setTimeout(() => {
        console.log(`Attempting to reconnect WebSocket (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`)
        connectWebSocket()
      }, 5000 * reconnectAttempts) // 재시도 간격 증가
    } else {
      appStore.showNotification({ message: 'WebSocket 재연결에 실패했습니다. 페이지를 새로고침해주세요.', type: 'error' })
    }
  }

  socket.value.onerror = (error) => {
    console.error('WebSocket error:', error)
    websocketStatus.value = 'disconnected' // 에러 발생 시 연결 끊김으로 처리
    // onclose에서 재연결 시도하므로 여기서는 알림만
    appStore.showNotification({ message: 'WebSocket 연결 중 오류가 발생했습니다.', type: 'error' })
  }
}

// 문서 검색 관련
const searchQuery = ref('')
const searchResults = ref([]) // { id: string, title: string, snippet: string, type: string, score: number, lastModified: string }[]
const isSearching = ref(false)
const searchError = ref('')
const searchAttempted = ref(false) // 검색 시도 여부
const searchPage = ref(1)
const searchPageSize = ref(10)
const hasMoreSearchResults = ref(false)
const isLoadingMore = ref(false)

const handleSearch = async (loadMore = false) => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    searchError.value = '검색어를 입력해주세요.'
    searchAttempted.value = true
    return
  }

  if (!loadMore) {
    searchPage.value = 1
    searchResults.value = []
    isSearching.value = true
  } else {
    isLoadingMore.value = true
  }
  
  searchError.value = ''
  searchAttempted.value = true

  try {
    // 실제 검색 API 엔드포인트로 교체해야 합니다.
    const response = await axios.get('/api/documents/search', {
      params: {
        query: searchQuery.value,
        page: searchPage.value,
        pageSize: searchPageSize.value,
      },
    })
    console.log('Search results:', response.data)
    if (loadMore) {
        searchResults.value = [...searchResults.value, ...response.data.results]
    } else {
        searchResults.value = response.data.results
    }
    hasMoreSearchResults.value = response.data.pagination.hasMore
    
    if (!searchResults.value.length && !loadMore) {
      // 검색 결과 없음 메시지 핸들링은 템플릿에서 처리
    }
  } catch (error) {
    console.error('Search failed:', error)
    searchError.value = error.response?.data?.message || error.message || '검색 중 오류가 발생했습니다.'
    appStore.showNotification({ message: `검색 실패: ${searchError.value}`, type: 'error' })
  } finally {
    isSearching.value = false
    isLoadingMore.value = false
  }
}

const loadMoreSearchResults = () => {
    if (hasMoreSearchResults.value && !isLoadingMore.value) {
        searchPage.value++
        handleSearch(true)
    }
}

const viewDocument = (documentId) => {
  // 실제 문서 상세 보기 라우트로 변경 필요
  router.push(`/documents/${documentId}`) 
}

// 검색어 하이라이팅 함수
const highlightMatches = (text, query) => {
  if (!query || !text) return text
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\\$&')})`, 'gi')
  return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-700 rounded">$1</mark>')
}

// 검색어 변경 시 선택된 파일 초기화 (옵션)
watch(searchQuery, () => {
    selectedFile.value = null
    uploadError.value = ''
    if (fileInput.value) fileInput.value.value = ''
})

// 기존 빠른 작업 함수 (예시)
const uploadDocument = (docType) => {
  console.log(`Quick upload for: ${docType}`)
  // 파일 선택창을 프로그래매틱하게 열거나, 특정 모달을 띄울 수 있습니다.
  // 여기서는 간단히 fileInput을 클릭하게 합니다.
  if (fileInput.value) {
    activeDocumentType.value = docType // 빠른 작업 버튼으로 문서 타입 미리 선택
    fileInput.value.click() 
  }
}

// 데이터 로딩 (예시)
const fetchStats = async () => {
  try {
    // const response = await axios.get('/api/stats') // 실제 통계 API
    // stats.value = response.data
    // 임시 데이터
    stats.value = {
      totalDocuments: 125,
      weeklyGrowth: 12,
      processedDocuments: 110,
      successRate: 95.5,
      generatedTemplates: 35,
      todayTemplates: 3,
      vectorEmbeddings: 10500,
    }
    documentTypes.value = [
      { id: 'noss_pdf', name: 'NOSS PDF', count: stats.value.totalDocuments }, // 예시로 전체 문서 수
      { id: 'excel_classification', name: '엑셀 분류', count: 50 },
      { id: 'word_template', name: '워드 템플릿', count: 20 },
    ]
  } catch (error) {
    console.error('Failed to fetch stats:', error)
    appStore.showNotification({ message: '통계 정보를 불러오는데 실패했습니다.', type: 'error' })
  }
}

onMounted(() => {
  connectWebSocket()
  fetchStats() // 컴포넌트 마운트 시 통계 정보 로드
})

onUnmounted(() => {
  if (socket.value) {
    socket.value.close()
  }
})

// activeDocumentType 변경 시 선택된 파일 초기화 (옵션)
watch(activeDocumentType, () => {
    selectedFile.value = null
    uploadError.value = ''
    if (fileInput.value) fileInput.value.value = ''
})
</script>

<style scoped>
/* Custom scrollbar */
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

/* Smooth transitions */
.transition-colors {
  transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

/* Clamp lines */
.clamp-lines-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}
</style>