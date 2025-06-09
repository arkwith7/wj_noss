#!/bin/bash
echo "🔄 Qdrant 재시작..."

./stop_qdrant.sh
./start_qdrant.sh
