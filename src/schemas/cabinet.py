from typing import Optional
from pydantic import BaseModel
from domains.cabinet import Cabinet


class CreateCabinet(BaseModel):
    cabinetName: str
    authorId: str
    description: Optional[str]

# no need to use DTO cause the project size is quite small
class CabinetResult(Cabinet):
    pass


class CabinetBulkResult(BaseModel):
    cabinets: list[CabinetResult]

