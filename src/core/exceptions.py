from enum import Enum
from typing import Any, Dict, Optional
from fastapi import status,Request
from pydantic import BaseModel

from core.generics import AppErrors, GenericServiceException,ServiceDTO, ServiceResult, isLeft, isRight


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

    @classmethod
    def create(cls,*args): 
        return cls(*args)

    def injectStatusCode(self):
        pass
    
    def resolveDTOMapping(self):
        print(self.TAG)


class DuplicatedError(CoreException):
    TAG = AppErrors.EMPTY
    def injectStatusCode(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
    

class AuthError(CoreException):
    TAG = AppErrors.AUTH
    def injectStatusCode(self):
        self.status_code = status.HTTP_403_FORBIDDEN


class NotFoundError(CoreException):
    TAG = AppErrors.EMPTY
    def injectStatusCode(self):
        self.status_code = status.HTTP_404_NOT_FOUND


class ValidationError(CoreException):
    TAG = AppErrors.VALIDATION
    def injectStatusCode(self):
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class ErrorDTOFactory:
    def __init__(self):
        self._DTO_Map = {}

    def registerErrorType(self,type_name:str , err_class_init ):
        self._DTO_Map[type_name] = err_class_init
    
    def create(self, key, **kwargs):
        builder = self._DTO_Map.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
    
    def fromServiceToWeb(self, wrapped_value : ServiceDTO):
        value = wrapped_value._value

        if isRight(wrapped_value) and isinstance(value,ServiceResult):
            # self._value.message.
            return value
        elif isLeft(wrapped_value) and isinstance(value,GenericServiceException):
            eType = value.errType;
            createErrObjFunc = self.create(eType, 
                                   message=value.message,
                                   title=value.errTitle);
            return createErrObjFunc
        else:
            return wrapped_value

DTO2HttpFactory = ErrorDTOFactory()

DTO2HttpFactory.registerErrorType(AppErrors.AUTH, AuthError.create)
DTO2HttpFactory.registerErrorType(AppErrors.VALIDATION, ValidationError.create)
DTO2HttpFactory.registerErrorType(AppErrors.EMPTY, DuplicatedError.create)
# DTO2HttpFactory.registerErrorType(AppErrors.DATA_ACCESS, DuplicatedError.create)

async def processDTOPacket(request: Request,call_next):
    response = await call_next(request)
    return DTO2HttpFactory.fromServiceToWeb(response)

# DTO2HttpFactory.registerErrorType("auth_error", AuthError)
# DTO2HttpFactory.registerErrorType("auth_error", AuthError)

