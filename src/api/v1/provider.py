from functools import lru_cache
from database.main import Database
from repository.adapters.auth_repo import AuthRepoImpl
from repository.adapters.user_repo import UserRepoImpl
from services.auth_services import AuthService
from services.user_services import UserService


db_container = Database()

authImpl = AuthRepoImpl(db_container.getSession())
userImpl = UserRepoImpl(db_container.getSession())
userService = UserService(repo=userImpl, authRepo=authImpl)

authService = AuthService(repo=authImpl)


@lru_cache
def getUserService():
    return userService


@lru_cache
def getAuthService():
    return authService
