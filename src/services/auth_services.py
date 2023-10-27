from typing import Protocol
from core.exceptions import AuthError
from core.utils.token import generateTokenSets
from domains.auth import TokenCredential, TokenEncryptor
from repository.protocols.auth_repo_meta import AuthRepo
from core.security import RefreshToken, TokenCipher


class AuthService:
    repo: AuthRepo
    cipher: TokenEncryptor

    def __init__(self, repo: AuthRepo):
        self.repo = repo
        self.cipher = TokenCipher()

    def rotateNewToken(self, refreshToken: str):
        rfTokenDecoded = RefreshToken.decode(refreshToken)
        bind_id = rfTokenDecoded.user_id

        _existedInWhitelist = self.repo.fetch_refresh_token(user_id=bind_id)

        if _existedInWhitelist is None:
            raise AuthError("Refresh token is not whitelisted!")

        tokenResult = generateTokenSets(bind_id)
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

        self.repo.append_refresh_token(bind_id, tkdCred)
        return tokenResult
