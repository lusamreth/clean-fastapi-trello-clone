from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4


class BoardPatcher(BaseModel):
    name: str | None = None
    topic: str | None = None
    description: str | None = None


class Board(BaseModel):
    boardId: str
    name: str
    topic: str
    description: Optional[str]
    cardRefs: list[str]
    modifiedOn: float
    createdOn: float

    @classmethod
    def create(cls, name: str, topic: str) -> "Board":
        bId = str(uuid4())
        tz = datetime.now().timestamp()

        return cls(
            name=name,
            boardId=bId,
            topic=topic,
            description=None,
            cardRefs=[],
            createdOn=tz,
            modifiedOn=tz,
        )

    def add_card(self, cardId: str):
        if self.cardRefs.count(cardId) > 0:
            raise Exception("Cannot append the existing card in the reference")

        self.cardRefs.append(cardId)

    def remove_card(self, cardId: str):
        if self.cardRefs.count(cardId) == 0:
            raise Exception("Cannot delete non-existing card in the reference")

        self.cardRefs.remove(cardId)
