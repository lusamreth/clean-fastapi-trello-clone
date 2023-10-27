from core.base_repo import BaseRepository
from abc import ABC, abstractmethod

from repository.model.cabinet import CabinetSchema
from domains.cabinet import Cabinet


class CabinetRepo(BaseRepository[CabinetSchema]):
    # @abstractmethod
    # def get_all_by_author(self, username: str) -> list[Cabinet] :
    #     pass

    @abstractmethod
    def db_to_entity(self, user_repo_data: CabinetSchema | None) -> Cabinet | None:
        pass

    @abstractmethod
    def entity_to_db(self, user_repo_data: Cabinet | None) -> CabinetSchema | None:
        pass

    @abstractmethod 
    def get_all_by_topic(self,topic:str) -> list[Cabinet] :
        pass
     
    @abstractmethod
    def get_all_by_user_id(self, user_id: str) -> list[Cabinet] :
        pass

