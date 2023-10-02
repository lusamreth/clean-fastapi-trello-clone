from core.base_repo import BaseRepository, ContextManagerRepository
from abc import ABC, abstractmethod

from repository.adapters.base_sql_repo import BaseRepo
from repository.model.user import UserSchema

# RepoDTO =


class UserRepo(BaseRepository[UserSchema]):
    @abstractmethod
    def get_by_username(self, username: str):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass

    # @abstractmethod
    # def reset_password(self,oldpassword:str , )
