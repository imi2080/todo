// 책임: 받은 데이터를 화면(DOM)으로 그리는 일만 담당한다. 서버 통신과 상태 관리는 하지 않는다.
// 사용자 입력은 textContent로만 넣는다. (innerHTML 사용 금지: XSS 방지)

function el(tag, { className, text, attrs } = {}) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  for (const [key, value] of Object.entries(attrs ?? {})) node.setAttribute(key, value);
  return node;
}

function button(label, className, onClick) {
  const btn = el("button", { className, text: label, attrs: { type: "button" } });
  btn.addEventListener("click", onClick);
  return btn;
}

function renderViewItem(todo, handlers) {
  const li = el("li", { className: todo.is_done ? "todo done" : "todo" });

  const checkbox = el("input", {
    attrs: { type: "checkbox", "aria-label": `${todo.title} 완료 표시` },
  });
  checkbox.checked = todo.is_done;
  checkbox.addEventListener("change", () => handlers.onToggle(todo.id, checkbox.checked));

  const body = el("div", { className: "todo-body" });
  body.append(el("span", { className: "todo-title", text: todo.title }));
  if (todo.note) body.append(el("span", { className: "todo-note", text: todo.note }));

  const actions = el("div", { className: "todo-actions" });
  actions.append(
    button("수정", "secondary", () => handlers.onEdit(todo.id)),
    button("삭제", "danger", () => handlers.onDelete(todo.id)),
  );

  li.append(checkbox, body, actions);
  return li;
}

function renderEditItem(todo, handlers) {
  const li = el("li", { className: "todo editing" });
  const form = el("form", { className: "edit-form" });

  const title = el("input", {
    attrs: { type: "text", required: "", maxlength: "200", "aria-label": "제목" },
  });
  title.value = todo.title;
  const note = el("input", {
    attrs: { type: "text", maxlength: "2000", placeholder: "메모", "aria-label": "메모" },
  });
  note.value = todo.note;

  const actions = el("div", { className: "todo-actions" });
  actions.append(
    el("button", { text: "저장", attrs: { type: "submit" } }),
    button("취소", "secondary", () => handlers.onCancelEdit()),
  );

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    handlers.onSave(todo.id, { title: title.value, note: note.value });
  });

  form.append(title, note, actions);
  li.append(form);
  // 편집 모드가 열리면 제목 입력창에 바로 커서를 둔다.
  queueMicrotask(() => title.focus());
  return li;
}

export function renderTodos(listEl, emptyEl, todos, editingId, handlers) {
  listEl.replaceChildren(
    ...todos.map((todo) =>
      todo.id === editingId ? renderEditItem(todo, handlers) : renderViewItem(todo, handlers),
    ),
  );
  emptyEl.hidden = todos.length > 0;
}

export function showError(errorEl, message) {
  errorEl.textContent = message;
  errorEl.hidden = !message;
}
