from fastapi import APIRouter, Depends

from api.v1.provider import getAuthService
from api.v1.resource.tags import RouterTag
from core.exceptions import AuthError, CoreException
from repository.adapters.auth_repo import AuthRepoImpl
from services.auth_services import AuthService

authRouter = APIRouter(tags=[RouterTag.AUTH])


@authRouter.post("/refresh")
def refreshToken(refresh_token: str, authService=Depends(getAuthService)):
    return authService.rotateNewToken(refresh_token)
