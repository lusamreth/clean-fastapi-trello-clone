from fastapi import APIRouter, Path, Query, Depends
from database.main import Database

from repository.adapters.base_sql_repo import BaseRepo
from repository.model.user import UserSchema
from ....schemas.user import RegistrationInfo
from services.user_services import UserService
from repository.adapters.user_repo import UserRepo, UserRepoImpl

# from ....services.user_services import c
from typing import Annotated

prefix = "/user"
userRouter = APIRouter(prefix=prefix, tags=["User"])
db_container = Database()


@userRouter.post("/")
async def register(
    userInfo: RegistrationInfo,
):
    impl = UserRepoImpl(db_container.getSession())
    service = UserService(repo=impl)
    result = service.register_user(userInfo)
    return result
