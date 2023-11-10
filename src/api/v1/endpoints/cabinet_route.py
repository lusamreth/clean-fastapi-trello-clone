from collections.abc import Callable
from fastapi import APIRouter, Depends, Path, Query, Response, Request
from typing import Annotated

from fastapi.routing import APIRoute

from api.v1.provider import getCabinetService, bearerSec

from schemas.cabinet import CreateCabinet, PatchCabinetInput
from services.cabinet_services import CabinetService


cabinetRouter = APIRouter(tags=["Cabinet"])


@cabinetRouter.post("/")
async def create_cabinet(
    cabInfo: CreateCabinet,
    token=Depends(bearerSec),
    cabService: CabinetService = Depends(getCabinetService),
):
    # user_id = "2fa97a0c-f540-4ac6-9cee-6b6a126225bc"
    user_id = token["user_id"]
    result = cabService.createCabinet(
        CreateCabinet(**{**cabInfo.model_dump(), "authorId": user_id})
    )
    return result.unwrap()


@cabinetRouter.get("/many")
async def fetch_cabinets(
    token=Depends(bearerSec),
    cabService: CabinetService = Depends(getCabinetService),
):
    # user_id = "2fa97a0c-f540-4ac6-9cee-6b6a126225bc"
    user_id = token["user_id"]
    result = cabService.getAllCabinets(user_id)
    return result.unwrap()


@cabinetRouter.delete("/{cabinet_id}")
async def delete_cabinets(
    cabinet_id: str,
    token=Depends(bearerSec),
    cabService: CabinetService = Depends(getCabinetService),
):
    result = cabService.deleteCabinet(cabinet_id)
    return result.unwrap()


@cabinetRouter.patch("/{cabinet_id}")
async def update_cabinet(
    cabinet_id: str,
    detail: PatchCabinetInput,
    _token=Depends(bearerSec),
    cabService: CabinetService = Depends(getCabinetService),
):
    result = cabService.updateCabinet(cabinet_id, detail)
    return result.unwrap()


# @cabinetRouter.post("/board/{cabinet_id}")
# async def pushcard(
#     cabinet_id :str,
#     token = Depends(bearerSec),
#     cabService: CabinetService=Depends(getCabinetService),
# ):
#     result = cabService.updateCabinet(cabinet_id);
#     return result.unwrap()


@cabinetRouter.get("/lists")
def main():
    pass
