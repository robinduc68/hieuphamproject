#!/bin/bash
# Script deploy lên VPS
# Chạy: bash deploy.sh

set -e  # dừng nếu có lỗi

echo "==> Pulling latest code..."
git pull origin main

echo "==> Checking .env file..."
if [ ! -f ".env" ]; then
  echo "ERROR: File .env không tồn tại!"
  echo "Chạy: cp .env.production.example .env rồi điền giá trị thật vào"
  exit 1
fi

echo "==> Building & starting containers..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

echo "==> Waiting for services to be healthy..."
sleep 5

echo "==> Container status:"
docker compose ps

echo ""
echo "✓ Deploy xong!"
echo "  Site:  https://hahoatsilk.com"
echo "  Admin: https://admin.hahoatsilk.com"
