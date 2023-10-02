from sqlalchemy import select
from ..protocols.user_repo_meta import UserRepo
from ..model.user import UserSchema
from .base_sql_repo import BaseRepo

# class UserRepoImpl(UserRepo):
#     def get_by_username(self, username: str):
#         return ""

#     def get_by_email(self, email: str):
#         return ""


class UserRepoImpl(BaseRepo[UserSchema], UserRepo):
    def __init__(self, session_factory):
        super().__init__(
            model=UserSchema, session_factory=session_factory
        )

    def get_by_username(self, username: str):
        with self.session_factory() as session:
            isExisted = session.query(self.model).filter(
                self.model.username == username
            )
            return isExisted

    def get_by_email(self, email: str):
        with self.session_factory() as session:
            isExisted = (
                session.query(self.model)
                .filter(self.model.email == email)
                .first()
            )
            print("exia", isExisted, email)
            return isExisted
