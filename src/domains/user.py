from pydantic import BaseModel, EmailStr, SecretStr
from core.exceptions import AuthError
from core.security import getPasswordHash
from email_validator import validate_email
from uuid import uuid4


class User(BaseModel):
    userId: str
    username: str
    email: EmailStr
    password: SecretStr

    @classmethod
    def _is_password_match(
        cls, password1: str, password2: str
    ) -> bool:
        return password1 == password2

    @classmethod
    def _verify_email_address(cls, email: str) -> str:
        if len(email) < 5:
            raise Exception(
                "Email address should be greater than 5 characters"
            )

        checkProperEmail = email.split("@")
        emailSplit = len(checkProperEmail)
        emailErr = None

        validatedEmail = validate_email(email)
        email = validatedEmail.normalized

        if emailSplit < 2:
            emailErr = "must contain @ sign in email address"
        elif emailSplit > 2:
            emailErr = "must not contain more than one @ sign in email address"
        else:
            pass
        if emailErr is not None:
            raise Exception(
                "{}{}".format("Email address ", emailErr)
            )
        return email

    @classmethod
    def _verify_username_rule(cls, username: str) -> str:
        return username

    @classmethod
    def register(
        cls,
        password1: str,
        password2: str,
        email: str,
        username: str,
    ) -> "User":
        uniqueUserId = uuid4()
        if len(password1) < 8:
            raise Exception(
                "Password must be greater than 8 characters!"
            )

        email = cls._verify_email_address(email)

        if not cls._is_password_match(
            password1=password1, password2=password2
        ):
            raise AuthError("Password is not matched!")

        return cls(
            userId=uniqueUserId.__str__(),
            password=SecretStr(getPasswordHash(password1)),
            email=email,
            username=username,
        )

    @classmethod
    def create(
        cls,
        user_id: str,
        email: str,
        username: str,
        hashed_password: str,
    ) -> "User":
        valid_email = cls._verify_email_address(email)
        valid_username = cls._verify_username_rule(username)

        return cls(
            userId=user_id,
            password=SecretStr(hashed_password),
            email=valid_email,
            username=valid_username,
        )

    @classmethod
    def getSecretPassword(cls) -> str:
        return cls.password.get_secret_value()

