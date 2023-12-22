from core.base_repo import BaseRepository
from abc import ABC, abstractmethod

from repository.model.user import UserSchema
from domains.user import User


class UserRepo(BaseRepository[UserSchema]):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def db_to_entity(self, user_repo_data: UserSchema | None) -> User | None:
        pass
