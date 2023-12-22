from typing import Optional
from pydantic import BaseModel
from domains.board import Board


class CreateActionInput(BaseModel):
    pass


class SingleResult(BaseModel):
    pass


class BulkResult(BaseModel):
    count: int


class FetchActionBulks(BaseModel):
    limits: Optional[int]


class PatchActionInput(BaseModel):
    pass


class PatchActionOutput(BaseModel):
    id: str
    modified: bool


class RemoveActionOutput(BaseModel):
    id: str
    removed: bool
