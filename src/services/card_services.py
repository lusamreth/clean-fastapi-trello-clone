from sqlalchemy.orm.loading import instances

from core.generics import AppErrors, ServiceDTO, err, ok, runDomainService
from domains.card import Card
from repository.adapters.base_sql_repo import LazyResult
from repository.protocols.board_repo_meta import BoardRepo
from repository.protocols.card_repo_meta import CardRepo
from schemas.card import (
    CardResult,
    CreateCardInput,
    FetchCardResult,
    PatchCardInput,
    PatchCardOutput,
    RemoveCardOutput,
)


def printNotFoundMsg(entityName: str, id: str):
    return "{} with id of {} is not Found!".format(entityName, id)


class CardService:
    repo: CardRepo
    boardRepo: BoardRepo

    def __init__(self, repo: CardRepo, boardRepo: BoardRepo):
        self.repo = repo
        self.boardRepo = boardRepo

    def getAllCards(self, boardId: str):
        cardsLazyResult = self.boardRepo.get(
            boardId,
            lazy_options={
                "query": {
                    "field": "cards",
                    "select": {
                        "mapFn": lambda todos: list(
                            map(lambda todo: todo.todo_id, todos)
                        ),
                        "field": "todos",
                    },
                }
            },
        )

        if cardsLazyResult is None:
            return err(printNotFoundMsg("Board", boardId), AppErrors.EMPTY)

        if not isinstance(cardsLazyResult, LazyResult):
            return err(printNotFoundMsg("Board", boardId), AppErrors.EMPTY)

        def convertor(card_tuple):
            index, card = card_tuple
            entity = self.repo.db_to_entity(card, cardsLazyResult.selected[index])
            if entity is None:
                return err(printNotFoundMsg("Card", card.id), AppErrors.EMPTY)

            return CardResult(**entity.model_dump())

        # convertor = lambda card:
        cardList = list(map(convertor, enumerate(cardsLazyResult.data)))
        return ok(FetchCardResult(cards=cardList))

    # please implement lazy loading retrieval with the lazy = True option
    # in the base repo, because otherwise you will a problems loading
    # one-to-many relationship

    def createCard(self, card_data: CreateCardInput):
        boardId = card_data.boardId
        board = self.boardRepo.get(boardId)
        if board is None:
            return err(printNotFoundMsg("Board", boardId), AppErrors.EMPTY)

        domainData = Card.create(title=card_data.title, description=card_data.content)
        _result = self.repo.add(**self.repo.entity_to_db(boardId, domainData, True))
        return ok(CardResult(**domainData.model_dump()))

    def patchCard(self, cardId: str, card_data: PatchCardInput):
        _res = self.repo.update(cardId, card_data)
        if _res is None:
            return err(printNotFoundMsg("Card", cardId), AppErrors.EMPTY)

        return ok(PatchCardOutput(id=cardId, modified=_res, attributes=card_data))

    def deleteCard(self, cardId: str):
        _res = self.repo.remove(cardId)
        if _res is None:
            return err(printNotFoundMsg("Card", cardId), AppErrors.EMPTY)

        return ok(RemoveCardOutput(id=cardId, removed=_res))
