from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.orm import Session
from ..protocols import board_repo_meta
from ..adapters.base_sql_repo import BaseRepo
from ..model.board import Board


class BoardRepo(BaseRepo):
    def __init__(
        self,
        session_factory: Callable[
            ..., AbstractContextManager[Session]
        ],
    ):
        super().__init__(
            session_factory=session_factory, model=Board
        )
