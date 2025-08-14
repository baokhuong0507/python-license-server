#!/usr/bin/env bash
# Dừng ngay nếu có lỗi và in ra từng lệnh được chạy
set -o errexit
set -x

echo "--- Bắt đầu kiểm tra build ---"

echo "1. Liệt kê các file trong thư mục:"
ls -la

echo "2. Hiển thị nội dung file requirements.txt:"
cat requirements.txt

echo "3. Nâng cấp pip và cài đặt các thư viện:"
pip install --upgrade pip
pip install -r requirements.txt

echo "4. Kiểm tra các thư viện đã được cài đặt:"
pip freeze

echo "5. Chạy lệnh tạo CSDL (database migration):"
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

echo "--- Build script hoàn thành ---"