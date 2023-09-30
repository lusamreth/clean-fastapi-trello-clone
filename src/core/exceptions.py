from typing import Any, Dict, Optional
from fastapi import status
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    title: Optional[str]
    message: str


class ErrorLink(BaseModel):
    about: str
    error_type: str


class ErrorResponse(BaseModel):
    status: int
    detail: ErrorDetail
    links: ErrorLink


class CoreException(Exception):
    def __init__(
        self,
        message="Unknown exception occured!",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None,
        links: Optional[ErrorLink] = None,
    ):
        self.status_code = status_code
        self.injectStatusCode()

        self.message = message
        self.headers = headers

        self.links = links
        self.title = title

    def injectStatusCode(self):
        pass


class DuplicatedError(CoreException):
    def injectStatusCode(self):
        self.status_code = status.HTTP_400_BAD_REQUEST


class AuthError(CoreException):
    # def __init__(self, **args) -> None:
    #     super().__init__(status.HTTP_403_FORBIDDEN, **args)
    def injectStatusCode(self):
        self.status_code = status.HTTP_403_FORBIDDEN


class NotFoundError(CoreException):
    def injectStatusCode(self):
        self.status_code = status.HTTP_404_NOT_FOUND


class ValidationError(CoreException):
    def injectStatusCode(self):
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
