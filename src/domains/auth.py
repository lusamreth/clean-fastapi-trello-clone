from pydantic import BaseModel, SecretStr, computed_field
from typing import Optional, Protocol, TypeVar, runtime_checkable
from uuid import uuid4


@runtime_checkable
class TokenEncryptor(Protocol):
    def __init__(self):
        pass

    def encrypt(self, plainTextToken: str) -> str:
        raise NotImplemented()

    def decrypt(self, encryptedTxt: str) -> str:
        raise NotImplemented()

    def refreshCipher(self):
        raise NotImplemented()


# a token class for storing and tracking token in the database
class TokenCredential(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    jti: str
    tokenType: str
    tokenValue: SecretStr
    expireAt: int
    cipher: Optional[TokenEncryptor]

    @classmethod
    def create(
        cls,
        tokenType: str,
        tokenValue: str,
        expireAt: int,
    ) -> "TokenCredential":
        jti = uuid4()
        if len(tokenValue) < 1:
            raise Exception("Cannot accept empty token value")

        if len(tokenType) < 1:
            raise Exception("Must provide token type")

        return cls(
            jti=str(jti),
            tokenType=tokenType,
            tokenValue=SecretStr(tokenValue),
            expireAt=expireAt,
            cipher=None,
        )

    def inject_encryptor(self, enc: TokenEncryptor):
        self.cipher = enc
        return self

    def encrypt_token(self):
        if self.cipher is None:
            raise Exception("Please inject encryptor agent.")

        innerValue = self.tokenValue.get_secret_value()
        encrypted = self.cipher.encrypt(innerValue)
        print("enc", encrypted)
        self.tokenValue = SecretStr(encrypted)
        return self


class AccessTokenPayload(BaseModel):
    user_id: str


class RefreshTokenPayload(BaseModel):
    user_id: str
    jti: str


class TokenProto(Protocol):
    def __init__(
        self,
        payload: dict,
        expire_in: float,
        algorithm: str,
    ):
        pass

    def __call__(self):
        pass

    def decode(self):
        pass
