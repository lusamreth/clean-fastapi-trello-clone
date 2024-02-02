from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute

from api.v1.provider import bearerSec, getTodoService
from schemas.todo import CreateTodoInput, PatchTodoInput
from services.todo_services import TodoService

todoRouter = APIRouter(tags=["Todo"])


@todoRouter.get("/{card_id}")
def getAllTodos(
    board_id: str,
    todoService: TodoService = Depends(getTodoService),
):
    return todoService.getAllTodos(board_id).unwrap()


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
