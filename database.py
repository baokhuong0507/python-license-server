import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Tải các biến từ file .env (nếu có, để chạy local)
load_dotenv()

# Render sẽ cung cấp biến môi trường DATABASE_URL
# Nếu không có, dùng SQLite để test ở local
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./license_server.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Chỉ cần connect_args cho SQLite
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()