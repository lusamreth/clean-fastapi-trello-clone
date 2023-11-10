from core.generics import ServiceDTO, err, ok, runDomainService, AppErrors
from repository.protocols.board_repo_meta import BoardRepo
from domains.board import Board, BoardPatcher
from repository.protocols.cabinet_repo_meta import CabinetRepo
from schemas.board import (
    BoardBulkResult,
    FetchBoardBulks,
    BoardResult,
    CreateBoardInput,
)
from services.cabinet_services import CabinetService


class BoardService:
    repo: BoardRepo
    cabinetService: CabinetService

    def __init__(self, repo: BoardRepo, parentService: CabinetService):
        self.repo = repo
        self.cabinet = parentService

    def createBoard(self, board_data: CreateBoardInput) -> ServiceDTO:
        makeDomainObject = lambda: Board.create(
            name=board_data.name, topic=board_data.topic
        )
        entity = makeDomainObject()
        print("ENTITY", entity)
        # entity = runDomainService(makeDomainObject)
        dbSchema = self.repo.entity_to_db(board_data.cabinetId, entity, to_dict=True)
        self.repo.add(**dbSchema)

        self.cabinet.appendBoardToCabinet(board_data.cabinetId, entity.boardId)
        return ok(
            BoardResult(**entity.model_dump()),
            "successfully create a\
                  new board!",
        )

    def getAllBoard(self, fetcher: FetchBoardBulks):
        entity = Board.create(fetcher.name, fetcher.topic)
        # self.repo.add(self.repo.entity_to_db(fetcher.cabinet_id, entity, to_dict=True))
        # self.cabinet.appendBoardToCabinet(fetcher.cabinet_id)
        # self.repo.get
        pass
