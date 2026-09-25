import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    """테스트마다 새 인메모리 DB를 쓰고, get_db 의존성을 그 DB로 바꿔치기한다."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # 인메모리 DB를 모든 연결이 공유하도록 한다
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # with 블록을 쓰지 않으므로 lifespan(실제 todo.db 생성)은 실행되지 않는다.
    yield TestClient(app)
    app.dependency_overrides.clear()
