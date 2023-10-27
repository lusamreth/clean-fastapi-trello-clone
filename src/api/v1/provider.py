from functools import lru_cache
from database.main import Database
from repository.adapters.auth_repo import AuthRepoImpl
from repository.adapters.cabinet_repo import CabinetRepoImpl
from repository.adapters.user_repo import UserRepoImpl

from services.auth_services import AuthService
from services.user_services import UserService
from services.cabinet_services import CabinetService


db_container = Database()
session = db_container.getSession()

authImpl = AuthRepoImpl(session)
userImpl = UserRepoImpl(session)
cabinetImpl = CabinetRepoImpl(session)

userService = UserService(repo=userImpl, authRepo=authImpl)
authService = AuthService(repo=authImpl)
cabinetService = CabinetService(repo=cabinetImpl)

@lru_cache
def getUserService():
    return userService


@lru_cache
def getAuthService():
    return authService


@lru_cache
def getCabinetService():
    return cabinetService
