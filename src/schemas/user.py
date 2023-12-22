from pydantic import BaseModel


class FetchUserRequest(BaseModel):
    userId: str


class UserLoginResponse(BaseModel):
    tokenType: str
    accessToken: str
    refreshToken: str


class LoginInfoInput(BaseModel):
    email: str
    password: str


class RegistrationInfoInput(BaseModel):
    username: str
    email: str
    password1: str
    password2: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "hide@hide.com",
                "password1": "pw",
                "password2": "pw",
                "username": "hide",
            }
        }


class UserProfile(BaseModel):
    userId: str
    username: str
    email: str

    class Config:
        json_schema_extra = {
            "userId": "abc123",
            "username": "hidey",
            "email": "hidey@gmail.com",
        }


class UpdatePasswordHintRequest(BaseModel):
    recovery_email: str

    class Config:
        json_schema_extra = {
            "example": {
                "recovery_email": "hide@hide.com",
            }
        }

    pass


class UpdatePasswordRequest(BaseModel):
    password1: str
    password2: str

    class Config:
        json_schema_extra = {
            "example": {
                "password1": "pw",
                "password2": "pw",
            }
        }
