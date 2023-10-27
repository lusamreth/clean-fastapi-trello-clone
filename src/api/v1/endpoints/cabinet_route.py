from fastapi import APIRouter, Depends, Path, Query
from typing import Annotated
from api.v1.provider import getCabinetService

from schemas.cabinet import CreateCabinet
from services.cabinet_services import CabinetService

cabinetRouter = APIRouter(tags=["Cabinet"])


@cabinetRouter.post("/cabinet")
async def get_cabinet_root(
    cabInfo: CreateCabinet,
    cabService: CabinetService=Depends(getCabinetService),
):
    result = cabService.createCabinet(cabInfo);
    # await createBoard.execute({"bruh": 100})
    return result




@cabinetRouter.get("/{cabinet_id}")
async def find_cabinet(
    cabinet_id: Annotated[str, Path(title="bruh")]
):
    return "henlo"


@cabinetRouter.get("/lists")
def main():
    pass
