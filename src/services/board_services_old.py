from ..core.base_service import BaseService
from ..repository.protocols.board_repo_meta import BoardRepo
import uuid


class OperationState:
    message: str
    success: bool


class FetchBoardService(BaseService):
    repo: BoardRepo

    def __init__(self, repo):
        self.repo = repo

    async def execute(self, id: str):
        result = await self.repo.get(id)
        return result


class UpdateBoardService(BaseService):
    repo: BoardRepo

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    async def execute(self, detail):
        detail["id"] = uuid.uuid4().hex
        self.repo.add(detail)
        return {"success": True}


class CreateBoardService(BaseService):
    repo: BoardRepo

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    async def execute(self, detail):
        # detail["id"] = uuid.uuid4().hex
        result = self.repo.add(detail)
        return {"success": True, "result": result}
