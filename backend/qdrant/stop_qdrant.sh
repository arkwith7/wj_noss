#!/bin/bash
echo "🛑 Qdrant 중지..."

docker stop qdrant
docker rm qdrant

echo "✅ Qdrant가 중지되었습니다."
