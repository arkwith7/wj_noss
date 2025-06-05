# Frontend Architecture Options for NOSS System

## Option 1: React + FastAPI (권장)

### 프로젝트 구조
```
wj_noss_v2/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   │   ├── Upload/
│   │   │   │   ├── FileUpload.jsx
│   │   │   │   ├── ProgressBar.jsx
│   │   │   │   └── StatusIndicator.jsx
│   │   │   ├── Processing/
│   │   │   │   ├── ProcessingView.jsx
│   │   │   │   ├── LogViewer.jsx
│   │   │   │   └── ResultsDisplay.jsx
│   │   │   └── Layout/
│   │   │       ├── Header.jsx
│   │   │       ├── Sidebar.jsx
│   │   │       └── Footer.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── UploadPage.jsx
│   │   │   └── ResultsPage.jsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.js
│   │   │   ├── useFileUpload.js
│   │   │   └── useProcessingStatus.js
│   │   └── services/
│   │       ├── api.js
│   │       └── websocket.js
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

### 기술 스택
- **Frontend**: React 18 + TypeScript + Vite
- **UI Library**: Material-UI (MUI) 또는 Ant Design
- **State Management**: Zustand 또는 React Query
- **Real-time**: WebSocket + Socket.IO
- **Build Tool**: Vite (빠른 개발 서버)

### 주요 컴포넌트 예시

#### 1. 파일 업로드 컴포넌트
```jsx
// FileUpload.jsx
import React, { useState } from 'react';
import { Upload, Progress, Alert } from 'antd';
import { useFileUpload } from '../hooks/useFileUpload';

const FileUpload = () => {
  const { uploadFile, isUploading, progress, error } = useFileUpload();

  return (
    <div className="upload-container">
      <Upload.Dragger
        name="file"
        accept=".pdf"
        customRequest={uploadFile}
        showUploadList={false}
      >
        <p className="ant-upload-drag-icon">📄</p>
        <p className="ant-upload-text">
          클릭하거나 파일을 드래그하여 업로드
        </p>
        <p className="ant-upload-hint">
          NOSS PDF 파일만 업로드 가능합니다
        </p>
      </Upload.Dragger>
      
      {isUploading && (
        <Progress 
          percent={progress} 
          status="active"
          strokeColor={{
            '0%': '#108ee9',
            '100%': '#87d068',
          }}
        />
      )}
      
      {error && (
        <Alert 
          message="업로드 실패" 
          description={error} 
          type="error" 
          showIcon 
        />
      )}
    </div>
  );
};
```

#### 2. 실시간 처리 상태 컴포넌트
```jsx
// ProcessingStatus.jsx
import React from 'react';
import { Steps, Card, Spin } from 'antd';
import { useWebSocket } from '../hooks/useWebSocket';

const ProcessingStatus = ({ taskId }) => {
  const { status, currentStep, logs } = useWebSocket(taskId);

  const steps = [
    { title: 'PDF 업로드', description: '파일 업로드 완료' },
    { title: 'PDF 분석', description: 'AI 기반 텍스트 추출' },
    { title: 'Excel 처리', description: '교육과정 데이터 매칭' },
    { title: '문서 생성', description: 'Word 템플릿 기반 생성' },
  ];

  return (
    <div className="processing-container">
      <Card title="처리 진행 상황">
        <Steps current={currentStep} items={steps} />
        
        <div className="logs-container" style={{ marginTop: 24 }}>
          <Card 
            title="실시간 로그" 
            size="small"
            extra={status === 'processing' && <Spin size="small" />}
          >
            <div className="log-viewer">
              {logs.map((log, index) => (
                <div key={index} className="log-entry">
                  <span className="timestamp">{log.timestamp}</span>
                  <span className="message">{log.message}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </Card>
    </div>
  );
};
```

### 실시간 통신 Hook
```js
// useWebSocket.js
import { useState, useEffect } from 'react';
import io from 'socket.io-client';

export const useWebSocket = (taskId) => {
  const [status, setStatus] = useState('pending');
  const [currentStep, setCurrentStep] = useState(0);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const socket = io('ws://localhost:8000');
    
    socket.emit('join_task', taskId);
    
    socket.on('status_update', (data) => {
      setStatus(data.status);
      setCurrentStep(data.step);
    });
    
    socket.on('log_message', (data) => {
      setLogs(prev => [...prev, {
        timestamp: new Date().toLocaleTimeString(),
        message: data.message
      }]);
    });

    return () => socket.disconnect();
  }, [taskId]);

  return { status, currentStep, logs };
};
```

## Option 2: FastAPI + HTMX (최소 변경)

### 장점
- 기존 Jinja2 템플릿 재사용
- JavaScript 최소화
- 빠른 마이그레이션
- 서버 사이드 중심

### 구현 예시
```html
<!-- upload.html with HTMX -->
<div class="upload-form">
  <form 
    hx-post="/api/upload" 
    hx-encoding="multipart/form-data"
    hx-target="#result"
    hx-indicator="#spinner"
  >
    <input type="file" name="file" accept=".pdf" required>
    <button type="submit">업로드</button>
  </form>
  
  <div id="spinner" class="htmx-indicator">
    <div class="spinner"></div>
  </div>
  
  <div id="result"></div>
</div>

<!-- 실시간 업데이트 -->
<div 
  hx-get="/api/status/{{ task_id }}" 
  hx-trigger="every 2s"
  hx-target="#progress"
>
  <div id="progress"></div>
</div>
```

## Option 3: Next.js Full-Stack

### 장점
- 프론트엔드와 백엔드 통합
- 서버 사이드 렌더링
- API Routes 내장
- Vercel 배포 최적화

### 구조
```
wj_noss_nextjs/
├── pages/
│   ├── api/
│   │   ├── upload.js
│   │   ├── process.js
│   │   └── status/[taskId].js
│   ├── index.js
│   ├── upload.js
│   └── results.js
├── components/
├── lib/
└── public/
```

## 추천사항

### 🎯 단기 (빠른 마이그레이션)
**HTMX + FastAPI**: 기존 템플릿을 최대한 활용하면서 현대적 기능 추가

### 🚀 장기 (확장성 중심)
**React + FastAPI**: 완전한 SPA로 현대적 UI/UX 제공

### ⚡ 균형잡힌 선택
**Vue.js + FastAPI**: React보다 학습 곡선이 낮으면서도 현대적

## 구현 우선순위

1. **1단계**: FastAPI 백엔드 구축 + 기존 템플릿 유지
2. **2단계**: HTMX로 동적 기능 추가
3. **3단계**: React/Vue 컴포넌트로 점진적 교체
4. **4단계**: 완전한 SPA 전환

이렇게 단계적으로 접근하면 기존 기능을 유지하면서도 현대적인 UI로 발전시킬 수 있습니다.
