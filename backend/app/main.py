# 책임: FastAPI 앱 생성, 시작 시 테이블 생성, API 라우터 등록, 정적 파일(프론트엔드) 마운트
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  (모델을 import해야 Base.metadata에 테이블이 등록된다)
from app.db import Base, engine
from app.routers import todos

# backend/app/main.py 기준으로 두 단계 위(프로젝트 루트)의 frontend/ 폴더
STATIC_DIR = Path(__file__).resolve().parents[2] / "frontend"


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Personal TODO", lifespan=lifespan)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(todos.router)

# API 라우트를 먼저 등록한 뒤 마지막에 마운트해야 "/api/*" 경로가 정적 파일에 가려지지 않는다.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
