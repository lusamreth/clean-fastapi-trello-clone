from domains.user import User
from ..protocols.user_repo_meta import UserRepo
from ..model.user import UserSchema
from .base_sql_repo import BaseRepo


class UserRepoImpl(BaseRepo[UserSchema], UserRepo):
    def __init__(self, session_factory):
        super().__init__(
            model=UserSchema,
            session_factory=session_factory,
            primary_key_identifier="user_id",
        )

    def get_by_username(self, username: str) -> User | None:
        with self.session_factory() as session:
            isExisted = (
                session.query(self.model)
                .filter(self.model.username == username)
                .first()
            )

            return self.db_to_entity(isExisted)

    def get_by_email(self, email: str) -> User | None:
        with self.session_factory() as session:
            isExisted = (
                session.query(self.model)
                .filter(self.model.email == email)
                .first()
            )
            return self.db_to_entity(isExisted)

    def db_to_entity(self, user_repo_data) -> User | None:
        if user_repo_data is not None:
            return User.create(
                user_id=user_repo_data.user_id,
                username=user_repo_data.username,
                email=user_repo_data.email,
                hashed_password=user_repo_data.password,
            )
