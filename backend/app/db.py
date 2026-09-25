# 책임: DB 엔진·세션 생성과 요청별 세션 제공(get_db). HTTP는 알지 못한다.
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("TODO_DATABASE_URL", "sqlite:///./todo.db")

# SQLite는 기본적으로 생성한 스레드에서만 연결을 쓸 수 있다. FastAPI는 요청을 여러 스레드로 처리하므로 해제한다.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """요청마다 세션을 하나 열고, 응답이 끝나면 닫는다. (FastAPI 의존성)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
