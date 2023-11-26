import asyncio
from ....core.base_repo import BaseRepository
from ....domains.cabinet import Cabinet
import json
import pydantic
from typing import Optional, Protocol

MAIN_MOCK_FILE = "board-repo-test.json"


class JsonBoardRepo(BaseRepository):
    async def get(self, id: str) -> Optional[Cabinet]:
        if id == "":
            return None

        with open(MAIN_MOCK_FILE, "r") as f:
            content = f.read()
            board_obj = json.loads(content)

            for board in board_obj["data"]:
                if board["id"] == id:
                    return board

            raise Exception(
                "Board with the id of {} doesn't exist".format(id)
            )

    async def add(self, data) -> Optional[Cabinet]:
        file = open(MAIN_MOCK_FILE, "r+")
        content = file.read()
        # await asyncio.sleep(1)
        with open(MAIN_MOCK_FILE, "w+") as f:
            prev_data = []
            if len(content) != 0:
                board_obj = json.loads(content)
                prev_data = board_obj["data"]
                print("pd", prev_data)
                prev_data.append(dict(data))

            j_data = json.dumps({"data": prev_data}, indent=4)
            f.write(j_data)

    async def update(self, id: str, patch) -> Optional[Cabinet]:
        await asyncio.sleep(1)

    async def list(self) -> Optional[Cabinet]:
        await asyncio.sleep(1)
        file = open(MAIN_MOCK_FILE, "r+")
        content = file.read()
        inner_data = json.loads(content)
        return inner_data.data

    async def remove(self, id: str) -> Optional[Cabinet]:
        await asyncio.sleep(1)
        file = open(MAIN_MOCK_FILE, "r+")
        content = file.read()

        with open(MAIN_MOCK_FILE, "w+") as f:
            prev_data = []

            if len(content) != 0:
                board_obj = json.loads(content)
                prev_data = board_obj["data"]
                prev_data = filter(
                    lambda x: x["id"] != id, prev_data
                )

            j_data = json.dumps({"data": prev_data}, indent=4)
            f.write(j_data)
