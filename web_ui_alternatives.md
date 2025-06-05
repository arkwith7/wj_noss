# NOSS 웹 UI 개선 방안 및 대안 아키텍처

## 현재 상태 분석

### 기존 Flask 웹 UI의 한계점
- 단순한 파일 업로드 인터페이스만 제공
- 실시간 진행 상태 확인 불가
- 반응형 디자인 부족
- 사용자 경험이 제한적
- 모던한 UI/UX 부족

## 웹 UI 개선 대안

### 1. React + FastAPI 아키텍처 (권장)

#### 장점
- 현대적이고 반응형 UI
- 컴포넌트 기반 재사용성
- 실시간 상태 관리
- 풍부한 생태계
- TypeScript 지원

#### 구조
```
frontend/
├── src/
│   ├── components/
│   │   ├── FileUploader.tsx
│   │   ├── ProgressTracker.tsx
│   │   ├── ResultViewer.tsx
│   │   └── Dashboard.tsx
│   ├── hooks/
│   │   ├── useFileUpload.ts
│   │   └── useWebSocket.ts
│   ├── services/
│   │   └── api.ts
│   └── App.tsx
├── package.json
└── vite.config.ts
```

#### 예시 컴포넌트 (FileUploader.tsx)
```typescript
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface FileUploaderProps {
  onUploadStart: () => void;
  onUploadProgress: (progress: number) => void;
  onUploadComplete: (result: any) => void;
}

export const FileUploader: React.FC<FileUploaderProps> = ({
  onUploadStart,
  onUploadProgress,
  onUploadComplete
}) => {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setIsUploading(true);
    onUploadStart();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const progress = (progressEvent.loaded / progressEvent.total) * 100;
          onUploadProgress(progress);
        }
      });
      
      onUploadComplete(response.data);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setIsUploading(false);
    }
  }, [onUploadStart, onUploadProgress, onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    disabled: isUploading
  });

  return (
    <div 
      {...getRootProps()} 
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
        ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p className="text-blue-500">파일을 여기에 놓으세요...</p>
      ) : (
        <div>
          <p className="text-gray-600">PDF 또는 Excel 파일을 드래그하거나 클릭하여 업로드하세요</p>
          <p className="text-sm text-gray-400 mt-2">지원 형식: .pdf, .xlsx</p>
        </div>
      )}
    </div>
  );
};
```

### 2. HTMX + FastAPI 아키텍처 (빠른 개선)

#### 장점
- 기존 HTML 템플릿 재사용 가능
- 최소한의 JavaScript로 AJAX 기능
- 빠른 구현 가능
- 서버사이드 렌더링 유지

#### 개선된 템플릿 예시
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOSS 교육과정 생성기</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto">
            <!-- Header -->
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold text-white mb-4">
                    <i class="fas fa-graduation-cap mr-3"></i>
                    NOSS 교육과정 자동 생성기
                </h1>
                <p class="text-xl text-blue-200">PDF와 Excel 파일로 맞춤형 교육과정을 생성하세요</p>
            </div>

            <!-- Upload Form -->
            <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
                <form 
                    hx-post="/upload" 
                    hx-target="#results" 
                    hx-indicator="#loading"
                    enctype="multipart/form-data"
                    class="space-y-6"
                >
                    <div class="grid md:grid-cols-2 gap-6">
                        <!-- PDF Upload -->
                        <div class="space-y-4">
                            <label class="block text-white font-semibold">
                                <i class="fas fa-file-pdf mr-2 text-red-400"></i>
                                NOSS 기준서 (PDF)
                            </label>
                            <div class="relative">
                                <input 
                                    type="file" 
                                    name="pdf_file" 
                                    accept=".pdf"
                                    class="hidden" 
                                    id="pdf-upload"
                                    required
                                >
                                <label 
                                    for="pdf-upload" 
                                    class="flex items-center justify-center w-full h-32 border-2 border-dashed border-blue-300 rounded-lg cursor-pointer hover:border-blue-400 transition-colors"
                                >
                                    <div class="text-center">
                                        <i class="fas fa-cloud-upload-alt text-3xl text-blue-300 mb-2"></i>
                                        <p class="text-blue-200">PDF 파일 선택</p>
                                    </div>
                                </label>
                            </div>
                        </div>

                        <!-- Excel Upload -->
                        <div class="space-y-4">
                            <label class="block text-white font-semibold">
                                <i class="fas fa-file-excel mr-2 text-green-400"></i>
                                능력단위별 요소 (Excel)
                            </label>
                            <div class="relative">
                                <input 
                                    type="file" 
                                    name="excel_file" 
                                    accept=".xlsx,.xls"
                                    class="hidden" 
                                    id="excel-upload"
                                    required
                                >
                                <label 
                                    for="excel-upload" 
                                    class="flex items-center justify-center w-full h-32 border-2 border-dashed border-green-300 rounded-lg cursor-pointer hover:border-green-400 transition-colors"
                                >
                                    <div class="text-center">
                                        <i class="fas fa-cloud-upload-alt text-3xl text-green-300 mb-2"></i>
                                        <p class="text-green-200">Excel 파일 선택</p>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <div class="text-center">
                        <button 
                            type="submit" 
                            class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg"
                        >
                            <i class="fas fa-magic mr-2"></i>
                            교육과정 생성하기
                        </button>
                    </div>
                </form>

                <!-- Loading Indicator -->
                <div id="loading" class="htmx-indicator">
                    <div class="text-center py-8">
                        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
                        <p class="text-white mt-4">처리 중입니다. 잠시만 기다려주세요...</p>
                    </div>
                </div>

                <!-- Results -->
                <div id="results" class="mt-8"></div>
            </div>
        </div>
    </div>

    <script>
        // File upload feedback
        document.getElementById('pdf-upload').addEventListener('change', function(e) {
            const label = e.target.nextElementSibling;
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                label.innerHTML = `<div class="text-center"><i class="fas fa-file-pdf text-3xl text-red-400 mb-2"></i><p class="text-red-200">${fileName}</p></div>`;
            }
        });

        document.getElementById('excel-upload').addEventListener('change', function(e) {
            const label = e.target.nextElementSibling;
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                label.innerHTML = `<div class="text-center"><i class="fas fa-file-excel text-3xl text-green-400 mb-2"></i><p class="text-green-200">${fileName}</p></div>`;
            }
        });
    </script>
</body>
</html>
```

### 3. Next.js Full-Stack 아키텍처

#### 장점
- SSR/SSG 지원
- API Routes 내장
- 최적화된 성능
- SEO 친화적

#### 구조
```
nextjs-app/
├── pages/
│   ├── api/
│   │   ├── upload.ts
│   │   └── status.ts
│   ├── index.tsx
│   └── results/[id].tsx
├── components/
│   ├── FileUploader.tsx
│   ├── ProgressBar.tsx
│   └── ResultDisplay.tsx
├── lib/
│   ├── api.ts
│   └── utils.ts
└── styles/
    └── globals.css
```

### 4. Streamlit 웹 앱 (프로토타입용)

#### 장점
- Python 전용으로 빠른 개발
- 데이터 과학 친화적
- 내장 UI 컴포넌트
- 배포 간편

#### 예시 코드
```python
import streamlit as st
import tempfile
import os
from main import process_noss_documents

st.set_page_config(
    page_title="NOSS 교육과정 생성기",
    page_icon="🎓",
    layout="wide"
)

def main():
    st.title("🎓 NOSS 교육과정 자동 생성기")
    st.markdown("PDF와 Excel 파일을 업로드하여 맞춤형 교육과정을 생성하세요.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 NOSS 기준서 (PDF)")
        pdf_file = st.file_uploader(
            "PDF 파일을 선택하세요",
            type=['pdf'],
            key="pdf"
        )
    
    with col2:
        st.subheader("📊 능력단위별 요소 (Excel)")
        excel_file = st.file_uploader(
            "Excel 파일을 선택하세요",
            type=['xlsx', 'xls'],
            key="excel"
        )
    
    if pdf_file and excel_file:
        if st.button("🚀 교육과정 생성하기", type="primary"):
            with st.spinner('처리 중입니다...'):
                # 임시 파일 저장
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_path = os.path.join(temp_dir, pdf_file.name)
                    excel_path = os.path.join(temp_dir, excel_file.name)
                    
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_file.getbuffer())
                    
                    with open(excel_path, 'wb') as f:
                        f.write(excel_file.getbuffer())
                    
                    # 처리 실행
                    try:
                        result = process_noss_documents(pdf_path, excel_path)
                        
                        st.success("✅ 교육과정이 성공적으로 생성되었습니다!")
                        
                        # 결과 표시
                        st.subheader("📋 생성된 교육과정")
                        st.json(result)
                        
                        # 다운로드 버튼
                        if 'lesson_plan' in result:
                            st.download_button(
                                label="📥 교육과정 다운로드",
                                data=result['lesson_plan'],
                                file_name="noss_lesson_plan.txt",
                                mime="text/plain"
                            )
                    
                    except Exception as e:
                        st.error(f"❌ 처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
```

## 권장 구현 순서

### 1단계: HTMX 기반 개선 (1-2일)
- 기존 Flask 앱에 HTMX 적용
- 현대적인 스타일링 추가
- 실시간 피드백 구현

### 2단계: FastAPI 백엔드 구축 (3-5일)
- Flask를 FastAPI로 마이그레이션
- WebSocket 지원 추가
- API 문서화

### 3단계: React 프론트엔드 (1-2주)
- React 컴포넌트 개발
- 상태 관리 구현
- 사용자 인터페이스 완성

## 기술 스택 비교

| 특징 | HTMX + FastAPI | React + FastAPI | Next.js | Streamlit |
|------|----------------|-----------------|---------|-----------|
| 개발 속도 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 확장성 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 사용자 경험 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 유지보수성 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 학습 곡선 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 결론

**단기 개선**: HTMX + Tailwind CSS로 기존 템플릿을 현대화
**중장기 목표**: React + FastAPI로 완전한 SPA 구축
**프로토타입**: Streamlit으로 빠른 데모 버전 제작

각 방안의 구체적인 구현 가이드와 샘플 코드를 제공할 수 있습니다.
