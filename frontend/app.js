// 책임: api.js와 ui.js를 연결하고, 화면 상태(현재 목록, 편집 중인 항목)를 관리한다.
// 데이터의 진실은 서버(DB)에 있다. 여기서는 서버가 준 목록을 화면용으로 들고 있을 뿐이다.
import { createTodo, deleteTodo, listTodos, updateTodo } from "./api.js";
import { renderTodos, showError } from "./ui.js";

const listEl = document.getElementById("todo-list");
const emptyEl = document.getElementById("empty");
const errorEl = document.getElementById("error");
const addForm = document.getElementById("add-form");
const titleInput = document.getElementById("new-title");
const noteInput = document.getElementById("new-note");

let todos = [];
let editingId = null;

function render() {
  renderTodos(listEl, emptyEl, todos, editingId, {
    onToggle: (id, isDone) => run(() => updateTodo(id, { is_done: isDone })),
    onEdit: (id) => {
      editingId = id;
      render();
    },
    onCancelEdit: () => {
      editingId = null;
      render();
    },
    onSave: (id, changes) =>
      run(async () => {
        await updateTodo(id, changes);
        editingId = null;
      }),
    onDelete: (id) => run(() => deleteTodo(id)),
  });
}

// 서버에 변경을 요청한 뒤, 서버의 최신 목록을 다시 받아 그린다. 실패하면 메시지를 보여준다.
async function run(action) {
  try {
    await action();
    showError(errorEl, "");
  } catch (err) {
    showError(errorEl, err.message);
  }
  await reload();
}

async function reload() {
  try {
    todos = await listTodos();
  } catch (err) {
    showError(errorEl, `목록을 불러오지 못했습니다: ${err.message}`);
  }
  render();
}

addForm.addEventListener("submit", (event) => {
  event.preventDefault();
  run(async () => {
    await createTodo(titleInput.value, noteInput.value);
    titleInput.value = "";
    noteInput.value = "";
  });
  titleInput.focus();
});

reload();
