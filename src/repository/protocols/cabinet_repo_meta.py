from core.base_repo import BaseRepository
from abc import ABC, abstractmethod

from repository.model.cabinet import CabinetSchema
from domains.cabinet import Cabinet, CabinetPatcher


class CabinetRepo(BaseRepository[CabinetSchema]):
    @abstractmethod
    def db_to_entity(self, cabinet_repo_data: CabinetSchema | None) -> Cabinet | None:
        pass

    @abstractmethod
    def entity_to_db(
        self, cabinet_repo_data: Cabinet | None, to_dict: bool
    ) -> CabinetSchema | dict | None:
        pass

    @abstractmethod
    def get_all_by_topic(self, topic: str) -> list[Cabinet]:
        pass

    @abstractmethod
    def get_all_by_user_id(self, user_id: str) -> list[Cabinet]:
        pass

    @abstractmethod
    def update(self, board_id: str, Partial: CabinetPatcher) -> Cabinet:
        pass
