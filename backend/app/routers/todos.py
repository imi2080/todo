# 책임: /api/todos 엔드포인트. 요청 검증 결과를 받아 DB를 호출하고 HTTP 상태 코드를 결정한다.
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoOut, TodoUpdate

router = APIRouter(prefix="/api/todos", tags=["todos"])


def _get_or_404(db: Session, todo_id: int) -> Todo:
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")
    return todo


@router.get("", response_model=list[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    # 미완료 먼저, 그 안에서는 최신 항목이 위로 온다.
    stmt = select(Todo).order_by(Todo.is_done, Todo.id.desc())
    return db.scalars(stmt).all()


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(title=payload.title, note=payload.note)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = _get_or_404(db, todo_id)
    # exclude_unset: 클라이언트가 실제로 보낸 필드만 반영한다.
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = _get_or_404(db, todo_id)
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
