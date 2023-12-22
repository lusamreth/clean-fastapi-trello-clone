from core.utils.helpers import unwrapDBTimeSet, unwrapEntityTimeSet
from domains.card import Card, CardPatcher
from repository.model.card import CardSchema

from ..adapters.base_sql_repo import BaseRepo
from ..protocols.card_repo_meta import CardRepo


class CardRepoImpl(BaseRepo[CardSchema], CardRepo):
    def __init__(self, session_factory):
        super().__init__(
            model=CardSchema,
            session_factory=session_factory,
            primary_key_identifier="card_id",
        )

    def db_to_entity(
        self,
        db_model: CardSchema | None,
        to_dict: bool = True,
        todoRefs: list | None = [],
    ) -> Card | dict | None:
        # def dbmTodoConvertor(todo: TodoSchema) -> Todo:
        #     pass
        if db_model is not None:
            dbm = db_model
            param = {
                "cardId": dbm.card_id,
                "title": dbm.title,
                "description": dbm.title,
                "todoRefs": todoRefs,
                # "createdOn": float(dbm.created_on.timestamp()),
                **unwrapDBTimeSet(dbm).model_dump(),
            }
            if to_dict:
                return param
            else:
                return Card(**param)

    def entity_to_db(
        self, board_id: str, entity: Card | None, to_dict=False
    ) -> CardSchema | dict | None:
        if entity is not None:
            param = {
                "card_id": entity.cardId,
                "title": entity.title,
                "todos": entity.todoRefs,
                "description": entity.description,
                "board_id": board_id,
                **unwrapEntityTimeSet(entity).model_dump(),
            }

            if to_dict:
                return param
            else:
                return CardSchema(**param)
