from core.security import AccessToken
from repository.model.user import UserSchema
from core.base_service import BaseService
from repository.protocols.user_repo_meta import UserRepo
from schemas.user import (
    LoginInfo,
    RegistrationInfo,
    UpdatePasswordRequest,
)

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

    def login_user(self, loginInfo: LoginInfo):
        existed = self.repo.get_by_email(loginInfo.email)
        if existed is None:
            raise AuthError("Invalid Email or Password!")

        mendToken = AccessToken(
            {"email": loginInfo.email}, expire_in=600
        )

        return mendToken()
