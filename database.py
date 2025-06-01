from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv #для работы с сессиями БД
import os

load_dotenv()
# Настройка базы данных (SQLite)
DATABASE_URL = os.getenv("DATABASE_URL") #подгружаеи данные из .env
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для логов в консоль

# Базовый класс для моделей
Base = declarative_base()

# Создаем фабрику сессий
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    username = Column(String, nullable=True)
    api_key = Column(String, nullable=True)
    created_at = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)