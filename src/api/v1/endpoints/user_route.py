from fastapi import APIRouter, Path, Query, Depends
from database.main import Database

from repository.adapters.base_sql_repo import BaseRepo
from repository.model.user import UserSchema
from ....schemas.user import LoginInfo, RegistrationInfo
from services.user_services import UserService
from repository.adapters.user_repo import UserRepo, UserRepoImpl


# PRIMARY TASKS :
# design api response model (based on jsonapi.org)
# rework registration route
# rework login route
# make common repo DTO model
# find a way to create refresh token
# coordinate authorization strategy
# find what access token payload store ( data-structure )
# find what refresh token payload store ( data-structure )
# explore fastapi features such as security modules(fastapi.security) and
# more useful utils

# from ....services.user_services import c
from typing import Annotated

prefix = "/user"
userRouter = APIRouter(prefix=prefix, tags=["User"])
db_container = Database()


impl = UserRepoImpl(db_container.getSession())
service = UserService(repo=impl)


@userRouter.post("/register")
async def register(
    userInfo: RegistrationInfo,
):
    result = service.registerUser(userInfo)
    return result


@userRouter.post("/login")
async def login(
    userInfo: LoginInfo,
):
    result = service.loginUser(userInfo)
    return result
