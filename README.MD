# NOSS (National Occupational Skills Standard) 교육과정 자동 생성 시스템

## 📋 프로젝트 개요

이 프로젝트는 NOSS (National Occupational Skills Standard) PDF 문서와 Excel 데이터를 분석하여 자동으로 교육과정 계획서(Lesson Plan)를 생성하는 지능형 웹 애플리케이션입니다. 

**현재 상태**: Flask 기반 웹 애플리케이션
**전환 계획**: **Vue.js 3 + FastAPI** 풀스택 아키텍처로 현대화 예정

Google의 Gemini AI를 활용하여 PDF에서 역량 단위 정보를 자동 추출하고, Excel 데이터와 매칭하여 실습용(LPP)과 이론용(LPT) 교육과정 문서를 자동 생성합니다.

## 🎯 주요 기능

- **🔍 PDF 분석**: NOSS PDF 문서에서 역량 단위(Competency Unit) 정보 자동 추출
- **📊 Excel 처리**: 교육과정 데이터가 포함된 Excel 파일 처리 및 매칭
- **🤖 AI 기반 데이터 추출**: Google Gemini AI를 활용한 구조화된 데이터 추출
- **📝 템플릿 기반 문서 생성**: Word 템플릿을 활용한 교육과정 계획서 자동 생성
- **🎨 현대적 웹 UI**: Vue.js 3 기반 반응형 사용자 인터페이스
- **⚡ 실시간 처리**: WebSocket을 통한 실시간 상태 업데이트 및 진행률 표시
- **📱 반응형 디자인**: 모바일, 태블릿, 데스크톱 최적화
- **🔐 보안**: JWT 인증 및 파일 업로드 보안

## 🏗️ 현재 프로젝트 구조 (Flask 기반)

```
wj_noss/
├── main.py                     # 메인 처리 로직 (콘솔용)
├── main_test.py               # 테스트 처리 로직
├── app.py                     # Flask 웹 애플리케이션
├── competency_unit.py         # 데이터 모델 클래스
├── process_pdf.py             # PDF 처리 모듈
├── process_excel.py           # Excel 처리 모듈
├── create_lesson_plan.py      # 교육과정 생성 모듈
├── requirements.txt           # Python 의존성
├── input/                     # 입력 파일 디렉토리
│   ├── cu_excel_sheets/       # 역량 단위별 Excel 시트
│   └── uploads/               # 업로드된 파일
├── output/                    # 생성된 파일
├── templates/                 # Flask HTML 템플릿
│   ├── upload.html            # 기본 업로드 페이지
│   ├── upload_htmx.html       # HTMX 기반 업로드 페이지
│   └── lesson_plan_templates/ # Word 템플릿
│       ├── lpp/               # 실습용 교육과정 템플릿
│       └── lpt/               # 이론용 교육과정 템플릿
└── README.md                  # 프로젝트 문서
```

## 🔮 개선된 프로젝트 구조 (Vue.js + FastAPI, Hybrid RAG)

```
wj_noss/
├── frontend/                    # Vue.js 3 Frontend
│   ├── public/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/
│   │   ├── router/
│   │   ├── services/
│   │   ├── composables/
│   │   └── assets/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                     # FastAPI Backend (Hybrid RAG)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI 진입점
│   │   ├── config.py           # 환경설정 (AI 서비스 타입 등)
│   │   ├── dependencies.py
│   │   ├── models/             # Pydantic 모델
│   │   │   ├── __init__.py
│   │   │   ├── enhanced_competency_unit.py # 확장 데이터 모델
│   │   │   ├── requests.py
│   │   │   └── responses.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── upload.py
│   │   │   │   │   ├── processing.py
│   │   │   │   │   ├── files.py
│   │   │   │   │   ├── ai_switch.py      # AI 서비스 선택/상태
│   │   │   │   │   └── websocket.py
│   │   │   │   └── api.py
│   │   ├── services/           # 비즈니스 로직 (계층별 분리)
│   │   │   ├── document_processing/
│   │   │   │   ├── enhanced_pdf_processor.py
│   │   │   │   ├── azure_openai_data_extractor.py
│   │   │   │   └── ollama_data_extractor.py
│   │   │   ├── knowledge_management/
│   │   │   │   └── rag_knowledge_manager.py
│   │   │   ├── template_engine/
│   │   │   │   └── smart_template_engine.py
│   │   │   ├── pdf_service.py
│   │   │   ├── excel_service.py
│   │   │   ├── lesson_plan_service.py
│   │   │   └── websocket_service.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── events.py
│   │   │   └── exceptions.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_utils.py
│   │       └── validation.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── shared/                     # 공통 타입 정의 (TypeScript)
│   └── types/
│       ├── api.ts
│       └── models.ts
│
├── input/                      # 입력 파일 디렉토리
├── output/                     # 생성된 파일
├── templates/                  # Word 템플릿
├── docker-compose.yml          # 전체 서비스 오케스트레이션
├── .env.example                # 환경 변수 예시 (AI 서비스 타입, DB 등)
└── README.md
```

### 🧠 AI 서비스 및 데이터베이스 계층

- **AI 서비스**: Azure OpenAI, Ollama(로컬 LLM), Hybrid(선택적)
- **Vector DB**: Qdrant
- **Metadata DB**: PostgreSQL
- **캐시/큐**: Redis, Celery

### 🏗️ 서비스 계층별 주요 모듈

- **Document Processing**: PDF/Excel 추출, AI 기반 구조화, 품질 검증
- **Knowledge Management (RAG)**: 벡터 임베딩, 하이브리드 검색, 재순위화
- **Template Engine**: 템플릿 기반 문서 생성, AI 콘텐츠 생성, 품질 평가
- **AI Switch**: Azure/Ollama/Hybrid 선택 및 상태 관리

### ⚙️ 환경설정 예시 (.env.example)

```
AI_SERVICE_TYPE=hybrid   # azure | ollama | hybrid
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
QDRANT_URL=http://qdrant:6333
POSTGRES_URL=postgresql://user:pass@db:5432/wj_noss
REDIS_URL=redis://redis:6379/0
```

### 🐳 docker-compose.yml 주요 서비스

- fastapi-backend (backend/app)
- vue-frontend (frontend)
- qdrant (벡터DB)
- postgres (메타데이터DB)
- redis (캐시/큐)
- ollama (로컬 LLM, 선택적)

### 🚀 실행 방법 (개발/운영)

```bash
# Backend 실행
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend 실행
cd frontend
npm run dev

# 전체 서비스 (Docker)
docker-compose up -d
```

### 📦 데이터 모델 (예시: EnhancedCompetencyUnit)

- Pydantic 기반, 메타데이터/품질/매칭정보 포함 (README 하단 참고)

### 📝 참고

- AI 서비스 타입은 config.py 및 .env에서 손쉽게 전환 가능
- 하이브리드 모드: 일반 문서는 Azure, 민감 문서는 Ollama로 자동 라우팅
- 서비스별 상세 구현 및 API 문서는 `/docs` (FastAPI)에서 확인

---