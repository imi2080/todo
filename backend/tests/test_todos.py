def create(client, title="우유 사기", **extra):
    return client.post("/api/todos", json={"title": title, **extra})


def test_create_returns_201_and_todo(client):
    res = create(client, "  우유 사기  ", note="2L")
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "우유 사기"  # 앞뒤 공백 제거
    assert body["note"] == "2L"
    assert body["is_done"] is False
    assert body["id"] > 0


def test_list_puts_open_todos_first_and_newest_first(client):
    a = create(client, "A").json()
    b = create(client, "B").json()
    client.patch(f"/api/todos/{a['id']}", json={"is_done": True})
    c = create(client, "C").json()

    titles = [t["title"] for t in client.get("/api/todos").json()]
    assert titles == ["C", "B", "A"]  # 미완료(C, B: 최신순) 다음에 완료(A)
    assert c["id"] > b["id"]


def test_patch_updates_only_given_fields(client):
    todo = create(client, "원본", note="메모").json()

    res = client.patch(f"/api/todos/{todo['id']}", json={"is_done": True})
    assert res.status_code == 200
    assert res.json()["is_done"] is True
    assert res.json()["title"] == "원본"
    assert res.json()["note"] == "메모"

    res = client.patch(f"/api/todos/{todo['id']}", json={"title": "수정됨"})
    assert res.json()["title"] == "수정됨"
    assert res.json()["is_done"] is True


def test_delete_returns_204_and_removes(client):
    todo = create(client).json()
    assert client.delete(f"/api/todos/{todo['id']}").status_code == 204
    assert client.get("/api/todos").json() == []


def test_patch_and_delete_missing_return_404(client):
    assert client.patch("/api/todos/999", json={"is_done": True}).status_code == 404
    assert client.delete("/api/todos/999").status_code == 404


def test_empty_or_blank_title_is_422(client):
    assert create(client, "").status_code == 422
    assert create(client, "   ").status_code == 422


def test_too_long_title_is_422(client):
    assert create(client, "가" * 201).status_code == 422


def test_patch_rejects_null_and_blank_title(client):
    todo = create(client).json()
    assert client.patch(f"/api/todos/{todo['id']}", json={"title": None}).status_code == 422
    assert client.patch(f"/api/todos/{todo['id']}", json={"title": "  "}).status_code == 422
