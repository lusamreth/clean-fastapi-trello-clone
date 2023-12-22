from fastapi import APIRouter, Header, Path, Query, Depends

from core.exceptions import AuthError, CoreException
from core.utils.exception_handler import exceptionHandler
from services.user_services import UserService
from ....schemas.user import LoginInfoInput, RegistrationInfoInput
from core.security import JWTBearer
from ..provider import getUserService, bearerSec


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

# from ....userServices.user_services import c

userRouter = APIRouter(tags=["User"])


@exceptionHandler([CoreException, AuthError])
@userRouter.post("/register")
async def register(
    userInfo: RegistrationInfoInput,
    userService: UserService = Depends(getUserService),
):
    result = userService.registerUser(userInfo)
    return result.unwrap()


@exceptionHandler([AuthError])
@userRouter.post("/login")
async def login(userInfo: LoginInfoInput, userService=Depends(getUserService)):
    result = userService.loginUser(userInfo)
    return result.unwrap()


# dependencies=[Depends(bearerSec)]
@exceptionHandler(CoreException)
@userRouter.get("/me")
async def profile(
    token=Depends(bearerSec), userService: UserService = Depends(getUserService)
):
    result = userService.getProfile(token["user_id"], scope=["email"])
    return result.unwrap()
