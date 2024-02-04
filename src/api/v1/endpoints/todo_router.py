from fastapi import APIRouter, Depends

from api.v1.provider import bearerSec, getTodoService
from api.v1.resource.prefixes import RouterPrefix
from api.v1.resource.tags import RouterTag
from schemas.todo import CreateTodoInput, PatchTodoInput
from services.todo_services import TodoService

todoRouter = APIRouter(tags=[RouterTag.TODO])
todoSharedRouter = APIRouter(tags=[RouterTag.TODO])


@todoSharedRouter.get("/{card_id}" + RouterPrefix.TODO)
def getAllTodos(
    card_id: str,
    todoService: TodoService = Depends(getTodoService),
):
    return todoService.getAllTodos(card_id).unwrap()


@todoRouter.post("/")
def createTodo(
    # board_id: str,
    todo_data: CreateTodoInput,
    todoService: TodoService = Depends(getTodoService),
):
    return todoService.createTodo(todo_data).unwrap()


@todoRouter.delete("/{todo_id}")
def deleteTodo(
    # board_id: str, delete_todo: DeleteTodoInput,
    todo_id: str,
    todoService: TodoService = Depends(getTodoService),
):
    return todoService.deleteTodo(todo_id).unwrap()


@todoRouter.patch("/{todo_id}")
def patchTodo(
    todo_id: str,
    todo_patch: PatchTodoInput,
    todoService: TodoService = Depends(getTodoService),
):
    return todoService.patchTodo(todo_id, todo_patch).unwrap()
