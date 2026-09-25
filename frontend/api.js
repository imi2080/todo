// 책임: 서버(API)와의 통신만 담당한다. DOM을 다루지 않고, 화면 상태도 모른다.

async function request(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    throw new Error(await errorMessage(res));
  }
  // 204 No Content(삭제)는 본문이 없다.
  return res.status === 204 ? null : res.json();
}

// FastAPI 에러 형식: {"detail": "메시지"} 또는 검증 실패 시 {"detail": [{"msg": ...}]}
async function errorMessage(res) {
  try {
    const body = await res.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) return body.detail.map((d) => d.msg).join(", ");
  } catch {
    // 본문이 JSON이 아니면 아래 기본 메시지를 쓴다.
  }
  return `요청 실패 (HTTP ${res.status})`;
}

export const listTodos = () => request("/api/todos");

export const createTodo = (title, note) =>
  request("/api/todos", { method: "POST", body: JSON.stringify({ title, note }) });

export const updateTodo = (id, changes) =>
  request(`/api/todos/${id}`, { method: "PATCH", body: JSON.stringify(changes) });

export const deleteTodo = (id) => request(`/api/todos/${id}`, { method: "DELETE" });
