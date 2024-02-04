from fastapi import APIRouter, Depends

from api.v1.provider import bearerSec, getBoardService
from api.v1.resource.prefixes import RouterPrefix
from schemas.board import CreateBoardInput, PatchBoardInput
from services.board_services import BoardService

from ..resource.tags import RouterTag

boardRouter = APIRouter(tags=[RouterTag.BOARD])
boardSharedRouter = APIRouter(tags=[RouterTag.BOARD])


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


# boardRouter.prefix
@boardSharedRouter.get("/{cabinet_id}" + RouterPrefix.BOARD)
async def fetch_boards(
    cabinet_id: str,
    # fetchInfo: FetchBoardBulks,
    token=Depends(bearerSec),
    cabService: BoardService = Depends(getBoardService),
):
    result = cabService.getAllBoard(cabinet_id)
    return result.unwrap()


@boardRouter.delete("/{board_id}")
async def remove_boards(
    board_id: str,
    # fetchInfo: FetchBoardBulks,
    token=Depends(bearerSec),
    cabService: BoardService = Depends(getBoardService),
):
    result = cabService.deleteBoard(board_id)
    return result.unwrap()


@boardRouter.patch("/{cabinet_id}")
async def patch_board(
    board_id: str,
    patchInfo: PatchBoardInput,
    token=Depends(bearerSec),
    cabService: BoardService = Depends(getBoardService),
):
    result = cabService.patchBoard(board_id, PatchBoardInput(**patchInfo.dict()))
    return result.unwrap()
