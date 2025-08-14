#!/usr/bin/env bash
# Thoát ngay nếu có lỗi
set -o errexit

# Cài đặt các thư viện
pip install -r requirements.txt

# Chạy lệnh Python để tạo các bảng trong CSDL dựa trên models.py
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"