from core.base_repo import BaseRepository
from abc import ABC, abstractmethod
from repository.model.card import CardSchema
from domains.card import Card, CardPatcher


class CardRepo(BaseRepository[CardSchema]):
    @abstractmethod
    def db_to_entity(
        self, card_repo_data: CardSchema | None, todoRefs: list | None
    ) -> Card | None:
        pass

    @abstractmethod
    def entity_to_db(
        self, board_id: str, card_schema_data: Card | None, to_dict: bool
    ) -> CardSchema | dict | None:
        pass

    @abstractmethod
    def update(self, card_id: str, patch_card: CardPatcher) -> CardSchema | None:
        pass
