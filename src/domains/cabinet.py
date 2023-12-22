from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, create_model
from enum import Enum
from uuid import uuid4


class CabinetPatcher(BaseModel):
    name: str | None = None
    # topic: str | None = None
    description: str | None = None


class Cabinet(BaseModel):
    cabinetId: str
    name: str
    author: str
    boardRefs: list[str]
    createdOn: float
    modifiedOn: float

    @classmethod
    def create(cls, name: str, author: str) -> "Cabinet":
        tz = datetime.now().timestamp()
        cId = str(uuid4())
        return cls(
            name=name,
            author=author,
            cabinetId=cId,
            boardRefs=[],
            createdOn=tz,
            modifiedOn=tz,
        )

    def appendBoardRef(self, ref: str):
        if self.boardRefs.count(ref) > 0:
            raise Exception("Cannot append the existing board in the cabinet reference")
        self.boardRefs.append(ref)

    def deleteBoardRef(self, ref: str):
        if self.boardRefs.count(ref) == 0:
            raise Exception("Cannot delete non-existing board in the cabinet reference")
        self.boardRefs.remove(ref)

    @classmethod
    def patchCabinet(cls, old: "Cabinet", partial: CabinetPatcher) -> "Cabinet":
        patched = partial.model_dump(exclude_unset=True)
        return cls(**old.model_dump(), **patched)
