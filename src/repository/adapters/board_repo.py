from collections.abc import Callable
from contextlib import AbstractContextManager
from core.utils.helpers import unwrapDBTimeSet, unwrapEntityTimeSet

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
            primary_key_identifier="board_id",
        )

    def db_to_entity(
        self, board_repo_data: BoardSchema | None, cardRefs: list | None = []
    ):
        bd = board_repo_data
        if bd is not None:
            return Board(
                boardId=bd.board_id,
                name=bd.name,
                description=bd.description,
                topic=bd.topic,
                cardRefs=cardRefs,
                **unwrapDBTimeSet(bd).model_dump()
                # createdOn=0,
                # modifiedOn=
            )

    def entity_to_db(self, cabinet_id: str, board: Board, to_dict: bool = True):
        if to_dict:
            return {
                "board_id": board.boardId,
                "name": board.name,
                "description": board.description,
                "topic": board.topic,
                "cabinet_id": cabinet_id,
                **unwrapEntityTimeSet(board).model_dump(),
            }
        else:
            return BoardSchema(
                board_id=board.boardId,
                name=board.name,
                description=board.description,
                topic=board.topic,
                cabinet_id=cabinet_id,
            )
