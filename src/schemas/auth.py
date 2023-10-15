from pydantic import BaseModel


class TokenExpiration(BaseModel):
    refreshToken: int
    accessToken: int


class RotatedTokenResult(BaseModel):
    refreshToken: str
    accessToken: str
    tokenExpiration: TokenExpiration
    tokenType: str

    # @classmethod
    # def create(cls, rToken, aToken, tokenType) -> RotatedTokenResult:
    #     pass
