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
