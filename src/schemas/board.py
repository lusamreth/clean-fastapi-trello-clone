from typing import Optional
from pydantic import BaseModel
from domains.board import Board


class CreateBoardInput(BaseModel):
    cabinetId: str
    name: str
    topic: str
    description: Optional[str]


class BoardResult(Board):
    pass


class BoardBulkResult(BaseModel):
    boards: list[BoardResult]


class FetchBoardBulks(BaseModel):
    cabinet_id: str
    pass


class PatchBoardInput(BaseModel):
    name: str
    topic: str
    description: Optional[str]


class RemoveBoardOutput(BaseModel):
    removed: int
