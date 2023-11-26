import os
import jwt
import bcrypt
import base64

from typing import TypeVar
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette.requests import Request
from domains.auth import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenEncryptor,
    TokenProto,
)
from uuid import uuid4
from .exceptions import AuthError
import time
from configs.settings import getSettings
from Cryptodome.Cipher import AES


def getPasswordHash(plainPass: str) -> str:
    passBytes = plainPass.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passBytes, salt)
    return hashed.decode()


def comparePassHash(plainPass: str, hashed: str) -> bool:
    passBytes = plainPass.encode("utf-8")
    hashedBytes = hashed.encode("utf-8")
    return bcrypt.checkpw(passBytes, hashedBytes)


TK = TypeVar("TK")


tokenSettings = getSettings()


class AccessToken(TokenProto):
    expire: float

    def __init__(
        self,
        user_id: str,
        expire_in=tokenSettings.ACCESS_TOKEN_EXPIRATION_TIME,
        algorithm=tokenSettings.JWT_ALGORITHM,
    ):
        self.payload = AccessTokenPayload(user_id=user_id)
        self.algo = algorithm
        self.expire = float(expire_in)
        self.scope = ""

    def __call__(self):
        accessTokenPayload = {
            **self.payload.model_dump(),
            "exp": time.time() + self.expire,
            "iss": tokenSettings.JWT_ISSUER,
            # "iss": "reth.server.com",
        }

        if self.expire > 1800 and os.getenv("ENV", "0") == "1":
            raise ValueError("AccessToken cannot be longer than half an hour!")

        token = jwt.encode(
            accessTokenPayload,
            algorithm=self.algo,
            key=tokenSettings.JWT_ACCESS_TOKEN_SECRET,
        )
        return token

    @staticmethod
    def decode(token: str):
        decoded = decodeJWT(token, tokenSettings.JWT_ACCESS_TOKEN_SECRET)
        if decoded["iss"] != tokenSettings.JWT_ISSUER:
            raise Exception("Invalid issuer domain")
        return decoded


class RefreshToken(TokenProto):
    def __init__(
        self,
        user_id,
        expire_in=tokenSettings.REFRESH_TOKEN_EXPIRATION_TIME,
        algorithm=tokenSettings.JWT_ALGORITHM,
    ):
        token_claim_id = uuid4()
        self.payload = RefreshTokenPayload(user_id=user_id, jti=str(token_claim_id))
        self.algo = algorithm
        self.expire = float(expire_in)
        self.scope = ""

    def __call__(self):
        if self.expire < 1800:
            pass

        refreshTokenPayload = {
            **self.payload.dict(),
            "exp": time.time() + self.expire,
            "iss": tokenSettings.JWT_ISSUER,
        }

        token = jwt.encode(
            refreshTokenPayload,
            algorithm=self.algo,
            key=tokenSettings.JWT_REFRESH_TOKEN_SECRET,
        )

        return token

    @staticmethod
    def decode(token: str) -> RefreshTokenPayload:
        decoded = decodeJWT(token, tokenSettings.JWT_REFRESH_TOKEN_SECRET)

        if decoded["user_id"] is None:
            raise Exception("Invalid refresh token!")

        if decoded["jti"] is None:
            raise Exception("Refresh Token must come with valid jti!")

        return RefreshTokenPayload(user_id=decoded["user_id"], jti=decoded["jti"])


def decodeJWT(token: str, secret) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            key=secret,
            algorithms=[tokenSettings.JWT_ALGORITHM],
        )
        return decoded_token if decoded_token["exp"] >= time.time() else {}

    except Exception as e:
        raise e


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(
                    message="Invalid authentication scheme.",
                )

            decodedPayload = self.verify_jwt(credentials.credentials)
            if isinstance(decodedPayload, str):
                raise AuthError(
                    message="Invalid token or expired token : {}".format(
                        decodedPayload
                    ),
                )

            return decodedPayload
        else:
            raise AuthError(message="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> dict | str:
        try:
            return AccessToken.decode(jwt_token)
        except Exception as e:
            return str(e)


security_settings = getSettings()


class TokenCipher(TokenEncryptor):
    def __init__(self):
        self.nonce = None
        self.refreshCipher()

    def encrypt(self, plainTextToken: str):
        cypherText, tag = self.cipher.encrypt_and_digest(plainTextToken.encode())
        self.refreshCipher()
        return base64.encodebytes(cypherText)

    def decrypt(self, encryptedTxt: str):
        plainText = self.cipher.decrypt(encryptedTxt.encode())
        self.refreshCipher()
        return plainText.decode()

    def refreshCipher(self):
        self.cipher = AES.new(
            security_settings.AES_KEY.encode(), AES.MODE_EAX, nonce=self.nonce
        )
        self.nonce = self.cipher.nonce
