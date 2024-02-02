from pydantic import BaseModel

from domains.todo import Todo, TodoPatcher

from .base_crud import PatchActionOutput, RemoveActionOutput


class CreateTodoInput(BaseModel):
    name: str
    content: str
    cardId: str


class FetchTodoInput(BaseModel):
    card_id: str


class TodoResult(Todo):
    pass


class FetchTodoResult(BaseModel):
    cardList: list[TodoResult]


class PatchTodoInput(TodoPatcher):
    pass


class RemoveTodoOutput(RemoveActionOutput):
    pass


class PatchTodoOutput(PatchActionOutput):
    attributes: TodoPatcher
