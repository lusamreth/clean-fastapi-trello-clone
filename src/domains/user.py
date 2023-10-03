from pydantic import BaseModel
from core.exceptions import AuthError
from core.security import getPasswordHash


class User(BaseModel):
    username: str
    email: str
    password: str

    @classmethod
    def _is_password_match(
        cls, password1: str, password2: str
    ) -> bool:
        return password1 == password2

    @classmethod
    def create(
        cls,
        password1: str,
        password2: str,
        email: str,
        username: str,
    ) -> "User":
        if len(password1) < 8:
            print("Password must be greater than 8 characters!")

        print(password1, password2, email)
        if not cls._is_password_match(
            password1=password1, password2=password2
        ):
            raise AuthError("Password is not matched!")

        return cls(
            password=getPasswordHash(password1),
            email=email,
            username=username,
        )
