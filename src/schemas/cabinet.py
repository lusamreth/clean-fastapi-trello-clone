from typing import Optional
from pydantic import BaseModel
from domains.cabinet import Cabinet,CabinetPatcher


class CreateCabinet(BaseModel):
    cabinetName: str
    authorId: str
    description: Optional[str]

class PatchCabinetInput(CabinetPatcher):
    pass

    # cabinetName: Optional[str]
    # author: Optional[str]
    # description: Optional[str]

# no need to use DTO cause the project size is quite small
class CabinetResult(Cabinet):
    pass


class CabinetBulkResult(BaseModel):
    cabinets: list[CabinetResult]


class CabinetRemovalResult(BaseModel):
    cabinetId : str
