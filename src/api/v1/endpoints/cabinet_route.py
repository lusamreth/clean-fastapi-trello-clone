from fastapi import APIRouter, Path, Query

# from ....services.assemble import createBoard, fetchBoard
from typing import Annotated

prefix = "/cabinet"
cabinetRouter = APIRouter(prefix=prefix, tags=["Cabinet"])


@cabinetRouter.get("/")
async def get_cabinet_root():
    # await createBoard.execute({"bruh": 100})
    print("res", 100)
    return "henlo"


@cabinetRouter.get("/{cabinet_id}")
async def find_cabinet(
    cabinet_id: Annotated[str, Path(title="bruh")]
):
    return "henlo"


@cabinetRouter.get("/lists")
def main():
    pass
