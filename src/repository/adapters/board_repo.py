from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.orm import Session

from repository.model.cabinet import BoardSchema
from ..protocols.board_repo_meta import BoardRepo
from ..adapters.base_sql_repo import BaseRepo
from domains.board import Board


class BoardRepoImpl(BaseRepo[BoardSchema], BoardRepo):
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
    ):
        super().__init__(
            session_factory=session_factory,
            model=BoardSchema,
            primary_key_identifier="cabinet_id",
        )

    def db_to_entity(self, board_repo_data: BoardSchema | None):
        bd = board_repo_data
        if bd is not None:
            return Board(
                boardId=bd.board_id,
                name=bd.name,
                description=bd.description,
                topic=bd.topic,
                cardRefs=[],
                createdOn=0,
            )

    def entity_to_db(self, cabinet_id: str, board: Board, to_dict: bool = True):
        if to_dict:
            return {
                "board_id": board.boardId,
                "name": board.name,
                "description": board.description,
                "topic": board.topic,
                # "cardRefs": [],
                "cabinet_id": cabinet_id,
            }
        else:
            return BoardSchema(
                board_id=board.boardId,
                name=board.name,
                description=board.description,
                topic=board.topic,
                cabinet_id=cabinet_id,
            )

    # def add(self, cabinet_id: str, detail: BoardSchema):
    #     with self.session_factory() as session:
    #         session.query(self.model.board_id)
    #         pass
    #     pass
