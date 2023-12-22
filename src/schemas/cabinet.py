from typing import Optional
from pydantic import BaseModel
from domains.cabinet import Cabinet, CabinetPatcher
from schemas.base_crud import PatchActionOutput


class CreateCabinet(BaseModel):
    name: str
    authorId: str
    description: Optional[str]


class CreateCabinetInput(BaseModel):
    name: str
    description: Optional[str]


class PatchCabinetInput(CabinetPatcher):
    pass


class PatchCabinetOutput(PatchActionOutput):
    attributes: CabinetPatcher


# no need to use DTO cause the project size is quite small
class CabinetResult(Cabinet):
    pass


class CabinetBulkResult(BaseModel):
    cabinets: list[CabinetResult]


class CabinetRemovalOutput(BaseModel):
    cabinetId: str
