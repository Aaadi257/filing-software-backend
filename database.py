import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔥 Determine database directory correctly
if getattr(sys, "frozen", False):
    # Packaged app
    db_dir = os.environ.get("APP_DB_PATH")
    if not db_dir:
        raise RuntimeError("APP_DB_PATH environment variable not set!")
else:
    # Development mode
    db_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure directory exists
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, "filing_system.db")

print("Database path being used:", db_path)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()