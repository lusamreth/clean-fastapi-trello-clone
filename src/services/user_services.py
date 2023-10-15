from typing import Optional
import typing
from pydantic import BaseModel
from core.generics import GenericHttpData
from core.security import TokenCipher
from core.utils.token import generateTokenSets
from domains.auth import TokenCredential
from repository.protocols.auth_repo_meta import AuthRepo
from repository.protocols.user_repo_meta import UserRepo
from schemas.user import (
    LoginInfoInput,
    RegistrationInfoInput,
    UpdatePasswordHintRequest,
    UpdatePasswordRequest,
    UserLoginResponse,
    UserProfile,
)

from core.exceptions import AuthError, ValidationError
from domains.user import User


class UserRegisterResponse(BaseModel):
    message: str


class UserService:
    repo: UserRepo
    authRepo: AuthRepo

    def __init__(self, repo: UserRepo, authRepo: AuthRepo):
        self.repo = repo
        self.authRepo = authRepo
        self.cipher = TokenCipher()

    def registerUser(self, registrationInfo: RegistrationInfoInput):
        email = registrationInfo.email
        existed = self.repo.get_by_email(email=email)

        try:
            userInfo = User.register(**registrationInfo.dict())
        except Exception as e:
            raise ValidationError(
                message=str(e),
                title="Domain Verification Error",
            )

        if existed is not None:
            raise AuthError("User is already existed !", title="Duplicated Error")
        _ = self.repo.add(
            **{
                **userInfo.model_dump(exclude={"userId"}),
                "user_id": userInfo.userId,
            }
        )
        return GenericHttpData(
            message="Registration success!",
            data=UserProfile(**userInfo.model_dump()).model_dump(),
        )

    def loginUser(self, loginInfo: LoginInfoInput):
        existed = self.repo.get_by_email(loginInfo.email)
        if existed is None:
            raise AuthError("Invalid Email or Password!", title="Unauthenticated")

        tokenResult = generateTokenSets(user_id=existed.userId, token_type="Bearer")
        refreshExpire = tokenResult.tokenExpiration.refreshToken

        tkdCred = (
            TokenCredential.create(
                tokenType=tokenResult.tokenType,
                tokenValue=tokenResult.refreshToken,
                expireAt=refreshExpire,
            )
            .inject_encryptor(self.cipher)
            .encrypt_token()
        )

        self.authRepo.append_refresh_token(existed.userId, tkdCred)
        return GenericHttpData(
            message="login was successfull!", data=tokenResult.dict()
        )

    def getProfile(self, user_id: str, scope: Optional[list[str]]) -> UserProfile:
        _db_existed = self.repo.get(user_id)
        userInfo = self.repo.db_to_entity(_db_existed)

        if _db_existed is None or userInfo is None:
            raise AuthError("Incorrect user id !!")

        return UserProfile(**userInfo.model_dump())

    # def recoverPassword(self, passInput: UpdatePasswordHintRequest):
    #     existed = self.repo.get_by_email(passInput.email)
    #     if existed:
    #         pass
    # if scope
