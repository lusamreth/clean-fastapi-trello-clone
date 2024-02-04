from core.generics import AppErrors, ServiceDTO, err, ok, runDomainService
from domains.board import Board, BoardPatcher
from repository.adapters.base_sql_repo import LazyResult
from repository.model.cabinet import CabinetSchema
from repository.protocols.board_repo_meta import BoardRepo
from repository.protocols.cabinet_repo_meta import CabinetRepo
from schemas.board import (
    BoardBulkResult,
    BoardResult,
    CreateBoardInput,
    PatchBoardInput,
    PatchBoardOutput,
    RemoveBoardOutput,
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

        # entity = runDomainService(makeDomainObject)
        dbSchema = self.repo.entity_to_db(board_data.cabinetId, entity, to_dict=True)
        self.repo.add(**dbSchema)
        # self.cabinet.appendBoardToCabinet(board_data.cabinetId, dbSchema)

        return ok(
            BoardResult(**entity.model_dump()),
            "successfully create a new board!",
        )

    def getAllBoard(self, cabinet_id: str):
        cid = cabinet_id
        # self.repo.add(self.repo.entity_to_db(fetcher.cabinet_id, entity, to_dict=True))
        lazy_result = self.cabinet.repo.get(
            cid,
            lazy_options={
                "query": {
                    "field": "boards",
                    "select": {
                        # "from": "boards",
                        "field": "cards",
                        "mapFn": lambda cards: list(
                            map(lambda card: card.card_id, cards)
                        ),
                    },
                },
            },
        )

        if lazy_result is None:
            return err(
                "Cabinet with the id {} is not found".format(cid),
                AppErrors.EMPTY,
            )

        if not isinstance(lazy_result, LazyResult):
            return err(
                "Cabinet with the id {} yield incorrect data access result".format(cid),
                AppErrors.INTERNAL,
            )

        db_result = lazy_result.data

        # cards = list(map(lambda card: card.id, board_db_data.cards))
        def board_db_to_entity(data_tuple):
            index, board_db_data = data_tuple
            return self.repo.db_to_entity(board_db_data, lazy_result.selected[index])

        boards = map(board_db_to_entity, enumerate(db_result))
        conv = lambda data: BoardResult(**data.model_dump())
        boardList = list(map(conv, boards))

        return ok(
            BoardBulkResult(boards=boardList, count=len(boardList)),
            "successfully fetch all boards",
        )

    def deleteBoard(self, boardId: str):
        db_result = self.repo.remove(boardId)
        if db_result is False:
            return err(
                "Board with the id {} is not found!".format(boardId),
                AppErrors.EMPTY,
            )
        return ok(RemoveBoardOutput(removed=1))

    def patchBoard(self, boardId: str, patches: PatchBoardInput):
        db_result = self.repo.update(boardId, patches)
        if db_result is False:
            return err(
                "Board with the id {} is not found!".format(boardId),
                AppErrors.EMPTY,
            )
        return ok(
            PatchBoardOutput(modified=db_result, boardId=boardId, attributes=patches)
        )
