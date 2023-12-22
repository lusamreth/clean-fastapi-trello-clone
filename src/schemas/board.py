from typing import Optional
from pydantic import BaseModel
from domains.board import Board, BoardPatcher
from schemas.base_crud import BulkResult, FetchActionBulks, CreateActionInput


class CreateBoardInput(CreateActionInput):
    cabinetId: str
    name: str
    topic: str
    description: Optional[str]


class BoardResult(Board):
    pass


class BoardBulkResult(BulkResult):
    boards: list[BoardResult]


class FetchBoardBulks(FetchActionBulks):
    cabinetId: str
    pass


class PatchBoardInput(BoardPatcher):
    pass
    # name: str
    # topic: str
    # description: Optional[str]


class PatchBoardOutput(BaseModel):
    boardId: str
    modified: int
    attributes: BoardPatcher


class RemoveBoardOutput(BaseModel):
    removed: int
