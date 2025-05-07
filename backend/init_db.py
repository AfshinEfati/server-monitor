from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import Base, User
import hashlib
import os

DATABASE_URL = "sqlite:///backend/db.sqlite3"

# حذف فایل قبلی (اختیاری)
if os.path.exists("backend/db.sqlite3"):
    os.remove("backend/db.sqlite3")
    print("🗑 Existing database removed.")

# ساخت دیتابیس و سشن
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("📦 Creating tables...")

# ساخت یوزر ادمین پیش‌فرض
username = "admin"
password = "admin123"
hashed = hashlib.sha256(password.encode()).hexdigest()
admin = User(username=username, hashed_password=hashed)
db.add(admin)
db.commit()

print(f"✅ Admin user created: username={username}, password={password}")
