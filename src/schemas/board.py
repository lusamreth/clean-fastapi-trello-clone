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


class FetchBoardBulks(Board):
    cabinet_id: str
    pass


class PatchBoardOutput(Board):
    pass
