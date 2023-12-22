from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4


class CardPatcher(BaseModel):
    title: str | None = None
    description: str | None = None


class Card(BaseModel):
    cardId: str
    title: str
    description: Optional[str]
    todoRefs: list[str]
    createdOn: float
    modifiedOn: float

    @classmethod
    def create(cls, title: str, description: str) -> "Card":
        cId = str(uuid4())
        tz = datetime.now().timestamp()

        return Card(
            cardId=cId,
            title=title,
            description=description,
            createdOn=tz,
            todoRefs=[],
            modifiedOn=tz,
        )

    def add_todo(self, todoId: str):
        if self.todoRefs.count(todoId) > 0:
            raise Exception("Cannot append the existing card in the reference")

        self.todoRefs.append(todoId)

    def remove_todo(self, todoId: str):
        if self.todoRefs.count(todoId) == 0:
            raise Exception("Cannot delete non-existing card in the reference")

        self.todoRefs.remove(todoId)
