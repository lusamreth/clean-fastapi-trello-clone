from abc import abstractmethod
from typing import Optional, Protocol
from pydantic import BaseModel
from ...domains.cabinet import Board
from ...core.base_repo import BaseRepository


class CreateBoardIn(BaseModel):
    name: str
    description: str
    topic: Optional[str]


class BoardRepo(BaseRepository[Board]):
    @abstractmethod
    def add(self, detail: CreateBoardIn):
        raise NotImplementedError()
