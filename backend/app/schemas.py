# 책임: API 요청/응답의 형태와 검증 규칙(Pydantic). 프론트-백엔드 계약이다.
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

# 앞뒤 공백을 제거한 뒤 1~200자여야 한다. 공백만 있는 제목은 422로 거절된다.
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Note = Annotated[str, StringConstraints(strip_whitespace=True, max_length=2000)]


class TodoCreate(BaseModel):
    title: Title
    note: Note = ""


class TodoUpdate(BaseModel):
    """부분 수정용. 보낸 필드만 바뀐다."""

    title: Title | None = None
    note: Note | None = None
    is_done: bool | None = None

    @field_validator("title", "note", "is_done")
    @classmethod
    def not_null_when_given(cls, value):
        # 필드를 아예 안 보내는 것은 허용하지만, 명시적으로 null을 보내는 것은 거절한다.
        if value is None:
            raise ValueError("null은 허용되지 않습니다")
        return value


class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    note: str
    is_done: bool
    created_at: datetime
    updated_at: datetime
