import jwt
import bcrypt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from .exceptions import AuthError
import time
from configs.settings import getSettings


def createAccessToken():
    pass


def getPasswordHash(plainPass: str) -> str:
    passBytes = plainPass.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passBytes, salt)
    return hashed.decode()


def comparePassHash(plainPass: str, hashed: str) -> bool:
    passBytes = plainPass.encode("utf-8")
    hashedBytes = hashed.encode("utf-8")
    return bcrypt.checkpw(passBytes, hashedBytes)


JWT_SECRET = "abci0wi20-1922%77362/.22./$*01*233++1"
# JWT_ALGORITHM = "RSA256"
JWT_ALGORITHM = "HS256"


class AccessTokenPayload:
    pass


tokenSettings = getSettings()


class AccessToken:
    expire: float

    def __init__(
        self,
        payload: dict,
        expire_in=900,
        algorithm=tokenSettings.JWT_ALGORITHM,
    ):
        self.payload = payload
        self.algo = algorithm
        self.expire = expire_in
        self.scope = ""

    def __call__(self):
        accessTokenPayload = {
            **self.payload,
            "exp": time.time() + self.expire,
            "iss": "reth.server.com",
        }

        if self.expire > 1800:
            raise Exception(
                "AccessToken cannot be longer than half an hour!"
            )

        token = jwt.encode(
            accessTokenPayload,
            algorithm=self.algo,
            key=tokenSettings.JWT_SECRET,
        )
        return token


class RefreshToken:
    expire: float

    def __init__(
        self, payload: dict, expire_in, algorithm=JWT_ALGORITHM
    ):
        self.payload = payload
        self.algo = algorithm
        self.expire = expire_in
        self.scope = ""

    def __call__(self):
        if self.expire < 1800:
            pass

        refreshTokenPayload = {
            **self.payload,
            "expire_in": time.time() + self.expire,
            "iss": "reth.server.com",
        }

        token = jwt.encode(
            refreshTokenPayload,
            algorithm=self.algo,
            key=JWT_SECRET,
        )
        return token


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )

        return (
            decoded_token
            if decoded_token["expires"] >= time.time()
            else {}
        )
    except Exception:
        return {}


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
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(
                    message="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise AuthError(message="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwt_token)
        except Exception:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
