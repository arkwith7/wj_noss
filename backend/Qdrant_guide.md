# 간단한 Qdrant Docker 설정 가이드

## 🐳 1. Docker 설치 (Debian 11)

### 빠른 Docker 설치

```bash
# Docker 설치 스크립트
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 재로그인 또는 그룹 권한 즉시 적용
newgrp docker

# 설치 확인
docker --version
```

## 🔍 2. Qdrant 실행 (매우 간단)

### 기본 실행 명령어

```bash
# Qdrant 컨테이너 시작
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# 상태 확인
docker ps

# 로그 확인
docker logs qdrant
```

### 웹 대시보드 접속

브라우저에서 http://localhost:6333/dashboard 접속

## 🛠️ 3. 간단한 관리 스크립트

### start_qdrant.sh

```bash
#!/bin/bash
echo "🚀 Qdrant 시작..."

# 기존 컨테이너가 있으면 제거
docker rm -f qdrant 2>/dev/null || true

# Qdrant 시작
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# 잠시 대기
sleep 3

# 상태 확인
if docker ps | grep -q qdrant; then
    echo "✅ Qdrant가 성공적으로 시작되었습니다!"
    echo "🌐 대시보드: http://localhost:6333/dashboard"
    echo "📡 API: http://localhost:6333"
else
    echo "❌ Qdrant 시작 실패"
    docker logs qdrant
fi
```

### stop_qdrant.sh

```bash
#!/bin/bash
echo "🛑 Qdrant 중지..."

docker stop qdrant
docker rm qdrant

echo "✅ Qdrant가 중지되었습니다."
```

### restart_qdrant.sh

```bash
#!/bin/bash
echo "🔄 Qdrant 재시작..."

./stop_qdrant.sh
./start_qdrant.sh
```

## 📦 4. Python 패키지 설치

### requirements.txt (Qdrant만 추가)

```bash
# 기존 패키지에 Qdrant 클라이언트만 추가
pip install qdrant-client==1.7.0

# 또는 requirements.txt에 추가
echo "qdrant-client==1.7.0" >> requirements.txt
pip install -r requirements.txt
```

## 🧪 5. 연결 테스트

### test_qdrant.py

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import numpy as np

def test_qdrant_connection():
    """Qdrant 연결 테스트"""
    try:
        # 클라이언트 생성
        client = QdrantClient("localhost", port=6333)
        
        # 기본 정보 확인
        print("✅ Qdrant 연결 성공!")
        
        # 컬렉션 목록 확인
        collections = client.get_collections()
        print(f"📂 현재 컬렉션 수: {len(collections.collections)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Qdrant 연결 실패: {e}")
        return False

def create_test_collection():
    """테스트 컬렉션 생성"""
    try:
        client = QdrantClient("localhost", port=6333)
        
        # 테스트 컬렉션 생성
        client.create_collection(
            collection_name="test_collection",
            vectors_config=VectorParams(
                size=384,  # sentence-transformers 임베딩 차원
                distance=Distance.COSINE
            )
        )
        
        print("✅ 테스트 컬렉션 생성 완료")
        return True
        
    except Exception as e:
        print(f"ℹ️ 컬렉션 생성: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Qdrant 연결 테스트 시작...")
    
    if test_qdrant_connection():
        create_test_collection()
        print("\n🎉 모든 테스트 완료!")
        print("🌐 대시보드에서 확인: http://localhost:6333/dashboard")
    else:
        print("\n❌ Qdrant가 실행 중인지 확인하세요.")
        print("실행 명령어: ./start_qdrant.sh")
```

## 🎯 6. 일상적인 사용법

### 개발 시작할 때

```bash
# 1. Qdrant 시작
./start_qdrant.sh

# 2. 연결 테스트
python test_qdrant.py

# 3. 개발 시작
cd ~/Dev/wj_noss/backend/app
source ../venv/bin/activate  # 가상환경 활성화
python main.py  # 또는 개발 서버 실행
```

### 개발 종료할 때

```bash
# Qdrant 중지 (선택적 - 계속 실행해도 됨)
./stop_qdrant.sh
```

### 문제 발생시

```bash
# Qdrant 재시작
./restart_qdrant.sh

# 로그 확인
docker logs qdrant

# 컨테이너 상태 확인
docker ps -a
```

## 📁 7. 파일 구조 (매우 단순)

```
~/Dev/wj_noss/
├── start_qdrant.sh          # Qdrant 시작 스크립트
├── stop_qdrant.sh           # Qdrant 중지 스크립트
├── restart_qdrant.sh        # Qdrant 재시작 스크립트
├── test_qdrant.py           # 연결 테스트
├── qdrant_storage/          # Qdrant 데이터 (자동 생성)
└── backend/
    ├── venv/                # Python 가상환경
    ├── requirements.txt     # Python 패키지
    └── app/
        └── main.py          # 메인 애플리케이션
```

## 🚀 8. 즉시 실행 가이드

### 현재 위치에서 바로 시작

```bash
cd ~/Dev/wj_noss

# 1. 스크립트 생성
cat > start_qdrant.sh << 'EOF'
#!/bin/bash
echo "🚀 Qdrant 시작..."
docker rm -f qdrant 2>/dev/null || true
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
sleep 3
if docker ps | grep -q qdrant; then
    echo "✅ Qdrant 시작 완료!"
    echo "🌐 대시보드: http://localhost:6333/dashboard"
else
    echo "❌ 시작 실패"
    docker logs qdrant
fi
EOF

cat > stop_qdrant.sh << 'EOF'
#!/bin/bash
echo "🛑 Qdrant 중지..."
docker stop qdrant && docker rm qdrant
echo "✅ 중지 완료"
EOF

# 2. 실행 권한 부여
chmod +x start_qdrant.sh stop_qdrant.sh

# 3. Qdrant 시작
./start_qdrant.sh

# 4. 연결 테스트
pip install qdrant-client
python -c "
from qdrant_client import QdrantClient
try:
    client = QdrantClient('localhost', port=6333)
    print('✅ Qdrant 연결 성공!')
    print('🌐 대시보드: http://localhost:6333/dashboard')
except Exception as e:
    print(f'❌ 연결 실패: {e}')
"
```

## 💡 9. 추가 팁

### 자동 시작 설정 (선택적)

```bash
# 시스템 부팅 시 Qdrant 자동 시작
docker update --restart unless-stopped qdrant
```

### 데이터 백업

```bash
# 데이터 백업
tar -czf qdrant_backup_$(date +%Y%m%d).tar.gz qdrant_storage/

# 데이터 복원
tar -xzf qdrant_backup_20241201.tar.gz
```

### 다른 포트 사용 (포트 충돌 시)

```bash
# 포트 변경 예시
docker run -d \
  --name qdrant \
  -p 7333:6333 \
  -p 7334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# Python 코드에서 포트 변경
client = QdrantClient("localhost", port=7333)
```

## ✅ 완료!

이제 Qdrant만 Docker로 실행하고, 나머지는 로컬 환경에서 개발할 수 있습니다.

**핵심 명령어 3개만 기억하세요:**
1. `./start_qdrant.sh` - 시작
2. `./stop_qdrant.sh` - 중지  
3. `http://localhost:6333/dashboard` - 대시보드

매우 간단하죠! 🎉