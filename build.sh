#!/usr/bin/env bash
# Dừng ngay lập tức nếu có lỗi
set -o errexit

# Nâng cấp pip và cài đặt các gói từ requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Chạy lệnh để tạo các bảng trong CSDL
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"