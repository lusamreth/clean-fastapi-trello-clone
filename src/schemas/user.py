from pydantic import BaseModel


class FetchUserRequest(BaseModel):
    userId: str


class LoginInfo(BaseModel):
    email: str
    password: str


class RegistrationInfo(BaseModel):
    username: str
    email: str
    password1: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "email": "hide@hide.com",
                "password1": "pw",
                "password2": "pw",
                "username": "hide",
            }
        }


class UpdatePasswordRequest(BaseModel):
    password1: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "password1": "pw",
                "password2": "pw",
            }
        }
