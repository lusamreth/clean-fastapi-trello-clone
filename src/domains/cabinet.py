from pydantic import BaseModel, create_model
from enum import Enum


class Cabinet(BaseModel):
    cabinet_id: str
    name: str
    board_refs: list[str]
    createdOn: str


class Board(BaseModel):
    board_id: str
    card_refs: list[str]
    topic: str
    description: str
    name: str
    createdOn: str


class Card(BaseModel):
    card_id: str
    description: str
    name: str
    todo_ref: list[str]
    createdOn: str


class TodoList(BaseModel):
    todo_id: str
    tasks: list[str]
    title: str
    createdOn: str


class ProgressStatus(str, Enum):
    COMPLETED = "completed"
    INPROGRESS = "inprogress"
    CANCELED = "canceled"


class Task:
    task_type: str
    content: str
    createdOn: str
    status: ProgressStatus
