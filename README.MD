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

## 🔮 계획된 프로젝트 구조 (Vue.js + FastAPI)

```
wj_noss/
├── frontend/                    # Vue.js 3 Frontend
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── main.js             # Vue 앱 진입점
│   │   ├── App.vue             # 루트 컴포넌트
│   │   ├── components/         # 재사용 가능한 컴포넌트
│   │   │   ├── FileUpload.vue  # 파일 업로드 컴포넌트
│   │   │   ├── ProcessStatus.vue # 처리 상태 컴포넌트
│   │   │   ├── FileList.vue    # 생성된 파일 목록
│   │   │   └── ProgressBar.vue # 진행률 표시 바
│   │   ├── views/              # 페이지 컴포넌트
│   │   │   ├── Home.vue        # 메인 페이지
│   │   │   ├── Dashboard.vue   # 대시보드
│   │   │   └── History.vue     # 처리 기록
│   │   ├── store/              # Pinia 상태 관리
│   │   │   ├── index.js
│   │   │   ├── modules/
│   │   │   │   ├── upload.js   # 업로드 상태
│   │   │   │   ├── processing.js # 처리 상태
│   │   │   │   └── files.js    # 파일 관리
│   │   ├── router/             # Vue Router
│   │   │   └── index.js
│   │   ├── services/           # API 서비스
│   │   │   ├── api.js          # Axios 인스턴스
│   │   │   ├── uploadService.js
│   │   │   ├── processingService.js
│   │   │   └── fileService.js
│   │   ├── composables/        # Vue 3 Composition API
│   │   │   ├── useWebSocket.js # WebSocket 훅
│   │   │   ├── useFileUpload.js # 파일 업로드 훅
│   │   │   └── useProcessing.js # 처리 로직 훅
│   │   └── assets/             # 정적 자원
│   │       ├── styles/
│   │       └── images/
│   ├── package.json
│   ├── vite.config.js          # Vite 설정
│   └── tailwind.config.js      # Tailwind CSS 설정
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI 애플리케이션 진입점
│   │   ├── config.py           # 설정 관리
│   │   ├── dependencies.py     # 의존성 주입
│   │   ├── models/             # Pydantic 모델
│   │   │   ├── __init__.py
│   │   │   ├── competency_unit.py # 데이터 모델
│   │   │   ├── requests.py     # API 요청 모델
│   │   │   └── responses.py    # API 응답 모델
│   │   ├── api/                # API 라우터
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── upload.py    # 파일 업로드 API
│   │   │   │   │   ├── processing.py # 처리 관련 API
│   │   │   │   │   ├── files.py     # 파일 관리 API
│   │   │   │   │   └── websocket.py # WebSocket 엔드포인트
│   │   │   │   └── api.py       # v1 API 라우터 통합
│   │   ├── services/           # 비즈니스 로직
│   │   │   ├── pdf_service.py  # PDF 처리 서비스
│   │   │   ├── excel_service.py # Excel 처리 서비스
│   │   │   ├── ai_service.py   # AI/Gemini 처리 서비스
│   │   │   ├── lesson_plan_service.py # 교육과정 생성 서비스
│   │   │   └── websocket_service.py # WebSocket 관리
│   │   ├── core/               # 핵심 기능
│   │   │   ├── __init__.py
│   │   │   ├── security.py     # 보안 및 인증
│   │   │   ├── events.py       # 이벤트 관리
│   │   │   └── exceptions.py   # 커스텀 예외
│   │   └── utils/              # 유틸리티
│   │       ├── __init__.py
│   │       ├── file_utils.py   # 파일 처리 유틸
│   │       └── validation.py   # 데이터 검증
│   ├── requirements.txt        # Python 의존성
│   └── Dockerfile             # 백엔드 컨테이너
│
├── shared/                     # 공통 타입 정의 (TypeScript)
│   └── types/
│       ├── api.ts
│       └── models.ts
│
├── input/                      # 입력 파일 디렉토리
│   ├── cu_excel_sheets/        # 역량 단위별 Excel 시트
│   └── uploads/                # 업로드된 파일
├── output/                     # 생성된 파일
├── templates/                  # Word 템플릿
│   ├── lpp/                    # 실습용 교육과정 템플릿
│   └── lpt/                    # 이론용 교육과정 템플릿
├── docker-compose.yml          # 개발 환경
├── .env.example               # 환경 변수 예제
└── README.md                  # 프로젝트 문서
```

## 🔧 현재 기술 스택

### 현재 사용 중 (Flask 기반)
- **Flask**: 경량 웹 프레임워크
- **Python 3.11+**: 메인 프로그래밍 언어
- **Google Generative AI (Gemini)**: AI 기반 텍스트 처리
- **PyPDF2**: PDF 처리
- **openpyxl**: Excel 파일 처리
- **python-docx**: Word 문서 처리
- **HTMX**: 동적 HTML 업데이트

### 🚀 전환 예정 기술 스택

#### Frontend (Vue.js 3)
- **Vue.js 3**: Composition API를 활용한 현대적 프론트엔드 프레임워크
- **Vite**: 빠른 개발 서버 및 빌드 도구
- **Pinia**: Vue 3 공식 상태 관리 라이브러리
- **Vue Router 4**: SPA 라우팅
- **Axios**: HTTP 클라이언트
- **Tailwind CSS**: 유틸리티 우선 CSS 프레임워크
- **HeadlessUI**: 접근성 좋은 UI 컴포넌트
- **Chart.js**: 데이터 시각화
- **Socket.io Client**: 실시간 통신

### Backend (FastAPI)
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **Python 3.11+**: 메인 프로그래밍 언어
- **Pydantic v2**: 데이터 검증 및 직렬화
- **SQLAlchemy**: ORM (선택적 데이터베이스 연동)
- **Celery + Redis**: 백그라운드 작업 처리
- **WebSocket**: 실시간 양방향 통신
- **Google Generative AI (Gemini)**: AI 기반 텍스트 처리
- **PyPDF2**: PDF 처리
- **openpyxl**: Excel 파일 처리
- **python-docx**: Word 문서 처리

### DevOps & Tools
- **Docker & Docker Compose**: 컨테이너화
- **Nginx**: 리버스 프록시 (프로덕션)
- **GitHub Actions**: CI/CD 파이프라인
- **Pytest**: 백엔드 테스트
- **Vitest**: 프론트엔드 테스트

### AI/ML
- **Google Gemini 1.5 Flash**: 텍스트 추출 및 구조화

## 📊 데이터 모델

### Competency Unit (역량 단위)
```python
class competency_unit:
    - program_code: 프로그램 코드
    - program_name: 프로그램 명
    - program_level: 수준
    - competency_unit_name: 역량 단위명
    - competency_unit_title: 역량 단위 제목
    - no_and_statement_of_work_activities: 작업 활동 목록
    - cu_excel_data: 연결된 Excel 데이터
```

### Lesson Plans
```python
class lesson_plan_practical:  # 실습용 교육과정
    - work_activities: 작업 활동
    - lp_title: 교육과정 제목
    - duration: 수업 시간
    - learning_objectives: 학습 목표

class lesson_plan_theory:     # 이론용 교육과정
    - work_activities: 작업 활동
    - lp_title: 교육과정 제목
    - duration: 수업 시간
    - learning_objectives: 학습 목표
```

## 🚀 설치 및 실행

### 현재 Flask 버전 실행

#### 1. 환경 설정
```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

#### 2. API 키 설정
Google AI API 키를 설정해야 합니다:
```python
# main.py 또는 main_test.py에서
GOOGLE_API_KEY = "your-api-key-here"
```

#### 3. 실행 방법

##### 웹 인터페이스 (권장)
```bash
python app.py
```
브라우저에서 `http://localhost:5000` 접속

##### 콘솔 실행
```bash
python main.py
```

### 🔮 Vue.js + FastAPI 전환 후 실행 (계획)

#### 개발 환경
```bash
# Backend 실행
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend 실행 (새 터미널)
cd frontend
npm run dev
```

#### Docker 환경
```bash
docker-compose up -d
```

## 🔄 처리 플로우

1. **PDF 업로드**: 사용자가 NOSS PDF 파일을 웹 인터페이스를 통해 업로드
2. **PDF 분석**: 
   - 목차(TOC) 분석하여 "Curriculum of Competency Unit" 섹션 찾기
   - 각 역량 단위별로 페이지 범위 분할
   - Gemini AI를 통해 구조화된 데이터 추출
3. **Excel 처리**: 
   - `input/cu_excel_sheets/` 디렉토리의 Excel 파일들 읽기
   - JPMPBP(실습) 및 JPMPBT(이론) 시트에서 교육과정 데이터 추출
4. **데이터 매칭**: PDF에서 추출한 역량 단위와 Excel 데이터 매칭
5. **문서 생성**: Word 템플릿을 기반으로 교육과정 계획서 생성

## 📁 입력 파일 형식

### PDF 파일
- NOSS 표준 형식의 PDF
- "Curriculum of Competency Unit" 섹션 포함
- 명확한 목차 구조 필요

### Excel 파일
- `input/cu_excel_sheets/` 디렉토리에 위치
- 다음 시트 포함:
  - **JPMPBP**: 실습용 교육과정 데이터
  - **JPMPBT**: 이론용 교육과정 데이터
- 각 시트는 다음 컬럼 구조:
  1. 순번
  2. 작업 활동 (Work Activities)
  3. 교육과정 제목 (LP Title)
  4. 수업 시간 (Duration)
  5. 학습 목표 (Learning Objectives)

## 🎨 현재 웹 인터페이스 특징

- **Flask 기반**: 서버 사이드 렌더링
- **HTMX 통합**: 동적 HTML 업데이트
- **반응형 디자인**: 다양한 화면 크기 지원
- **실시간 피드백**: 파일 처리 상태 표시
- **파일 목록**: 생성된 문서 목록 표시 및 다운로드

## 🔮 전환 후 웹 인터페이스 (계획)

- **Vue.js 3 SPA**: 클라이언트 사이드 렌더링
- **실시간 통신**: WebSocket을 통한 양방향 통신
- **현대적 UI**: Tailwind CSS와 애니메이션 효과
- **상태 관리**: Pinia를 통한 중앙집중식 상태 관리
- **진보된 사용자 경험**: 실시간 진행률, 알림, 드래그 앤 드롭

## 🛠️ 현재 주요 모듈

### 📄 process_pdf.py
- PDF 텍스트 추출 및 분석
- 목차(TOC) 파싱 및 페이지 분할
- Gemini AI를 통한 구조화된 데이터 추출

### 📊 process_excel.py  
- Excel 파일 읽기 및 파싱
- JPMPBP(실습) 및 JPMPBT(이론) 시트 처리
- 교육과정 데이터 추출 및 구조화

### 🏗️ competency_unit.py
- 데이터 모델 정의
- 역량 단위 및 교육과정 클래스
- 데이터 검증 로직

### 🌐 app.py
- Flask 웹 애플리케이션
- 파일 업로드 처리
- 웹 인터페이스 제공

## 🔄 현재 처리 플로우

- **다국어 지원**: 현재 영어/한국어 혼용, 완전 다국어 지원 가능
- **템플릿 커스터마이징**: 다양한 교육기관 템플릿 지원
- **배치 처리**: 여러 PDF 파일 동시 처리
- **데이터베이스 연동**: 처리 이력 및 결과 저장
- **API 확장**: RESTful API 제공

## ⚠️ 주의사항

1. Google AI API 키가 필요합니다
2. PDF 구조가 NOSS 표준을 따라야 합니다
3. Excel 파일은 지정된 형식을 준수해야 합니다
4. 대용량 파일 처리 시 시간이 오래 걸릴 수 있습니다

## 🤝 기여 방법

1. 이슈 제기 또는 기능 제안
2. 포크 후 개발
3. 테스트 진행
4. 풀 리퀘스트 제출

## 📄 라이선스

이 프로젝트는 교육 목적으로 개발되었습니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 등록해 주세요.

---

*자동 생성된 교육과정 계획서는 반드시 검토 후 사용하시기 바랍니다.*
