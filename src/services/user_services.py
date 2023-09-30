from repository.model.user import UserSchema
from core.base_service import BaseService
from repository.protocols.user_repo_meta import UserRepo
from schemas.user import RegistrationInfo, UpdatePasswordRequest
from core.exceptions import AuthError
from domains.user import User


class UserService:
    repo: UserRepo

    def __init__(self, repo: UserRepo):
        self.repo = repo

    def register_user(self, registrationInfo: RegistrationInfo):
        email = registrationInfo.email
        existed = self.repo.get_by_email(email=email)
        userInfo = User.create(**registrationInfo.dict())

        if existed is not None:
            raise AuthError("User is already existed !")

        return self.repo.add(**userInfo.dict())

    def login_user(self):
        pass
