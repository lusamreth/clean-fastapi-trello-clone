from core.base_repo import BaseRepository
from abc import ABC, abstractmethod

from repository.model.cabinet import BoardSchema
from domains.board import Board


class BoardRepo(BaseRepository[BoardSchema]):
    @abstractmethod
    def db_to_entity(
        self, cabinet_repo_data: BoardSchema | None, cardRefs: list | None
    ) -> Board | None:
        pass

    @abstractmethod
    def entity_to_db(
        self, cabinet_id: str, cabinet_repo_data: Board | None, to_dict: bool
    ) -> BoardSchema | dict | None:
        pass
