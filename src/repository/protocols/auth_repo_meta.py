from core.base_repo import BaseRepository
from abc import ABC, abstractmethod
from repository.model.auth import TokenSchema
from domains.auth import TokenCredential


class AuthRepo(BaseRepository[TokenSchema]):
    @abstractmethod
    def db_to_entity(
        self, user_repo_data: TokenSchema | None
    ) -> TokenCredential | None:
        pass

    def clear_token_group(self):
        pass

    def append_refresh_token(
        self, user_id: str, tokenCredential: TokenCredential
    ):
        pass

    def fetch_refresh_token(
        self, user_id: str
    ) -> TokenCredential | None:
        pass
