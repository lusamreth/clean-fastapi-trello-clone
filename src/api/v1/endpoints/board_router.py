from collections.abc import Callable
from fastapi import APIRouter, Depends, Path, Query, Response, Request
from typing import Annotated

from fastapi.routing import APIRoute

from api.v1.provider import getBoardService, getCabinetService, bearerSec

from schemas.board import CreateBoardInput
from services.board_services import BoardService


boardRouter = APIRouter(tags=["Board"])


@boardRouter.post("/")
async def create_board(
    cabInfo: CreateBoardInput,
    token=Depends(bearerSec),
    cabService: BoardService = Depends(getBoardService),
):
    # user_id = "2fa97a0c-f540-4ac6-9cee-6b6a126225bc"
    user_id = token["user_id"]
    result = cabService.createBoard(
        CreateBoardInput(**{**cabInfo.model_dump(), "authorId": user_id})
    )
    return result.unwrap()


@boardRouter.get("/many")
async def fetch_boards(
    token=Depends(bearerSec),
    cabService: BoardService = Depends(getBoardService),
):
    # user_id = "2fa97a0c-f540-4ac6-9cee-6b6a126225bc"
    user_id = token["user_id"]
    result = cabService.getAllBoard(user_id)
    return result.unwrap()


# @boardRouter.delete("/{board_id}")
# async def delete_boards(
#     board_id: str,
#     token=Depends(bearerSec),
#     cabService: CabinetService = Depends(getCabinetService),
# ):
#     result = cabService.deleteCabinet(board_id)
#     return result.unwrap()


# @boardRouter.patch("/{board_id}")
# async def update_board(
#     board_id: str,
#     detail: PatchCabinetInput,
#     _token=Depends(bearerSec),
#     cabService: CabinetService = Depends(getCabinetService),
# ):
#     result = cabService.updateCabinet(board_id, detail)
#     return result.unwrap()


# # @boardRouter.post("/board/{board_id}")
# # async def pushcard(
# #     board_id :str,
# #     token = Depends(bearerSec),
# #     cabService: CabinetService=Depends(getCabinetService),
# # ):
# #     result = cabService.updateCabinet(board_id);
# #     return result.unwrap()


# @boardRouter.get("/lists")
# def main():
#     pass
