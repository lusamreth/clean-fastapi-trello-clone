from pydantic import BaseModel
from .base_crud import RemoveActionOutput, PatchActionOutput
from domains.todo import Todo, TodoPatcher

# from domains.card import Todo, TodoPatcher


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
