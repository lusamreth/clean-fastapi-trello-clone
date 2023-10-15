from core.security import AccessToken, RefreshToken
from domains.auth import RefreshTokenPayload, TokenCredential
from repository.model.auth import TokenSchema
from schemas.auth import RotatedTokenResult, TokenExpiration


def generateTokenSets(user_id: str, token_type="Bearer"):
    generateAccessToken = AccessToken(user_id=user_id)
    generateRefreshToken = RefreshToken(user_id=user_id)

    newAToken = generateAccessToken()
    newRToken = generateRefreshToken()

    return RotatedTokenResult(
        refreshToken=newRToken,
        accessToken=newAToken,
        tokenExpiration=TokenExpiration(
            refreshToken=int(generateRefreshToken.expire),
            accessToken=int(generateAccessToken.expire),
        ),
        tokenType=token_type,
    )
