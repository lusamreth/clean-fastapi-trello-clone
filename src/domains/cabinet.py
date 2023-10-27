from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, create_model
from enum import Enum
from uuid import uuid4

class Cabinet(BaseModel):
    cabinetId: str
    name: str
    author : str
    boardRefs: list[str]
    createdOn: float

    @classmethod 
    def create(cls,name:str,author:str) -> "Cabinet":
        tz = datetime.now().timestamp()
        cId = str(uuid4())
        return cls(
                name=name,
                author=author,
                cabinetId=cId,
                boardRefs=[],
                createdOn=tz

            )

    def appendBoardRef(self,ref:str):
        self.boardRefs.append(ref)

class Board(BaseModel):
    boardId: str
    name: str
    cardRefs: list[str]
    topic: str
    description: Optional[str]
    createdOn: float

    @classmethod 
    def create(cls,name:str,topic:str) -> "Board":
        bId = str(uuid4())
        tz = datetime.now().timestamp()
        return cls(
            boardId= bId,
            name=name,
            topic=topic,
            description=None,
            cardRefs=[],
            createdOn=tz
        )

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
