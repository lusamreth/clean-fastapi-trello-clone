from typing import Optional
from pydantic import BaseModel
from core.generics import (
    Right,
    ServiceDTO,
    ServiceResult,
    err,
    ok,
    ErrorTitle,
    AppErrors,
)
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
            return err(str(e), AppErrors.VALIDATION, ErrorTitle.DOMAIN_ERROR)

        if existed is not None:
            # raise AuthError("User is already existed !", title="Duplicated Error")
            return err(
                "User is already existed !",
                AppErrors.AUTH,
                title=ErrorTitle.UNAUTHENTICATED,
            )

        _ = self.repo.add(
            **{
                **userInfo.model_dump(exclude={"userId"}),
                "user_id": userInfo.userId,
            }
        )

        return ok(
            msg="Registration success!",
            data=UserProfile(**userInfo.model_dump()).model_dump(),
        )

    def loginUser(self, loginInfo: LoginInfoInput) -> ServiceDTO:
        existed = self.repo.get_by_email(loginInfo.email)
        if existed is None:
            raise AuthError("Invalid Email or Password!", title="Unauthenticated")
        try:
            tokenResult = generateTokenSets(user_id=existed.userId, token_type="Bearer")
        except Exception as tkError:
            return err(AppErrors.AUTH, "Token failure: {}".format(tkError))

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

        _db_res = self.authRepo.append_refresh_token(existed.userId, tkdCred)
        return ok(msg="login was successfull!", data=tokenResult.dict())

    def getProfile(self, user_id: str, scope: Optional[list[str]]) -> ServiceDTO:
        _db_existed = self.repo.get(user_id)
        userInfo = self.repo.db_to_entity(_db_existed)

        if _db_existed is None or userInfo is None:
            raise AuthError("Incorrect user id !!")

        return ok(data=UserProfile(**userInfo.model_dump()))

    # def recoverPassword(self, passInput: UpdatePasswordHintRequest):
    #     existed = self.repo.get_by_email(passInput.email)
    #     if existed:
    #         pass
    # if scope
