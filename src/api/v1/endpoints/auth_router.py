from fastapi import APIRouter, Depends
from api.v1.provider import getAuthService
from services.auth_services import AuthService
from core.exceptions import AuthError, CoreException
from repository.adapters.auth_repo import AuthRepoImpl


authRouter = APIRouter(tags=["Auth"])


@authRouter.post("/refresh")
def refreshToken(
    refresh_token: str, authService=Depends(getAuthService)
):
    return authService.rotateNewToken(refresh_token)
