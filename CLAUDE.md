# CLAUDE.md

개인용 TODO 웹 서비스. 요구사항의 기준 문서는 `PRD.md`이다. 이 프로젝트는 **풀스택 구조(프론트엔드 - 백엔드 - API)를 직접 경험하며 학습하는 것**이 목적이므로, 빠른 완성보다 이해 가능한 구조를 우선한다.

## 현재 단계

- **M1 완료**: DB 모델, 할 일 CRUD API(`/api/todos`), 기본 화면 (F1)
- **다음: M2**: 마감일·우선순위(F2), 카테고리(F3)
- 단계가 바뀌면 이 항목을 갱신한다. (M1 → M2 → M3 → M4, 상세는 `PRD.md` 8절)

## 기술 스택

- 백엔드: FastAPI (Python 3.11+), Uvicorn
- DB: SQLite + SQLAlchemy
- 프론트엔드: HTML / CSS / Vanilla JavaScript (프레임워크·번들러 사용 금지)
- 테스트: pytest
- 정적 파일은 FastAPI `StaticFiles`로 서빙한다 (단일 프로세스).

## 프로젝트 구조

```
app/
  main.py       # FastAPI 앱, 라우터 등록, 정적 파일 마운트
  db.py         # 엔진, 세션
  models.py     # SQLAlchemy 모델 (DB 매핑)
  schemas.py    # Pydantic 스키마 (API 계약)
  routers/      # todos.py, categories.py, auth.py
static/
  index.html    # 구조
  style.css     # 표현
  api.js        # 서버 통신(fetch)만 담당
  ui.js         # DOM 렌더링만 담당
  app.js        # api.js와 ui.js를 연결, 화면 상태 관리
tests/
```

## 실행 명령 (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload      # http://127.0.0.1:8000 , API 문서: /docs
pytest
```

## 계층 책임 원칙 (반드시 지킬 것)

- **프론트엔드**: 렌더링, 입력 처리, API 호출만 한다. 비즈니스 규칙을 두지 않는다.
- **routers/**: 요청 검증, 인증, HTTP 상태 코드 결정만 한다. SQL을 직접 쓰지 않는다.
- **models.py / db.py**: 저장과 조회만 한다. HTTP 개념(`Request`, 상태 코드)을 알지 못한다.
- **schemas.py**가 프론트-백엔드 계약이다. 스키마를 바꾸면 프론트 코드와 테스트에 미치는 영향을 함께 알려준다.
- 서버(DB)가 데이터의 진실의 원천이다. 프론트는 화면 상태만 가진다.

## 코딩 규칙

- Python: 타입 힌트를 사용하고 PEP 8을 따른다. 함수는 짧게 유지한다.
- API 경로는 `/api/` 접두사, 복수형 리소스명(`/api/todos`)을 사용한다.
- 에러 응답은 FastAPI 기본 형식(`{"detail": ...}`)과 적절한 상태 코드(400/401/404/422)를 사용한다.
- JavaScript: ES 모듈(`type="module"`), `const`/`let`, `async/await`를 사용한다.
- 사용자 입력을 DOM에 넣을 때는 `textContent`를 쓰고, `innerHTML`에 넣지 않는다 (XSS 방지).
- 각 파일 상단에 그 파일의 책임을 한 줄 주석으로 적는다.
- 설정값(DB 경로, 비밀번호 등)은 환경변수로 분리하고 코드에 하드코딩하지 않는다.
- 외부 라이브러리는 꼭 필요할 때만 추가하고, 추가 이유를 설명한다.

## 작업 방식 (학습 우선)

- 새 기능을 구현하기 전에 **프론트 / API / DB 각각에 필요한 변경을 먼저 요약**하고, 내 확인을 받은 뒤 구현한다.
- 한 번에 **한 계층, 한 기능** 단위로 작업한다. 요청하지 않은 기능이나 리팩터링을 끼워 넣지 않는다.
- 코드를 작성한 뒤에는 **요청이 처리되는 흐름을 짧게 설명**한다. 새 개념(Pydantic, 의존성 주입, 세션 등)은 처음 등장할 때 한두 문장으로 설명한다.
- 구현 후 확인 방법(`/docs`에서 호출, 브라우저 Network 탭 확인, pytest 명령)을 함께 알려준다.
- 기능 구현 시 해당 API의 pytest 테스트를 함께 작성한다.
- 내가 직접 수정해 보고 싶다고 하면 정답 코드 대신 힌트와 수정 위치를 알려준다.

## 범위 관리

- 핵심 기능은 5개(F1~F5)로 고정한다. 그 밖의 아이디어는 `PRD.md` 10절 오픈 이슈나 별도 백로그에 기록하고 구현하지 않는다.
- 비목표: 다중 사용자, 알림, 프레임워크(React/Vue), 번들러.

## 마일스톤 회고 (완료 시 아래에 3줄씩 추가)

<!-- 예시
### M0 (YYYY-MM-DD)
- 새로 이해한 것:
- Claude Code가 잘 도와준 점 / 아쉬운 점:
- 다음에 다르게 할 것:
-->
