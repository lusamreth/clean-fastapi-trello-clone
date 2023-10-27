from enum import Enum
from typing import Optional
from fastapi import Request
from pydantic import BaseModel
from oslash import Either
from collections.abc import Callable

DEFAULT_SUCCESS_MSG = "Request successfully fullfilled"

class ErrorTitle(Enum):
    DOMAIN_ERROR = "Domain Verification Error"
    UNAUTHENTICATED = "Unauthenticated"
    UNAUTHORIZED = "Unauthorized"
    TOKEN_ERROR = "Token Gen Error"
    UNKNOWN = "Unknown error"

class AppErrors: 
    AUTH = "auth_error"
    VALIDATION = "validation"
    EMPTY = "not_found"


class ServiceResult(BaseModel):
    message: str
    data : dict


class GenericServiceException(BaseModel):
    message: str
    errType : str
    errTitle : str

class ServiceDTO(Either):
    def __init__(self, value : ServiceResult | GenericServiceException):
        self._value = value

    def presenter(self):
        if isinstance(self._value, ServiceResult):
            # self._value.message.
            pass
        elif isinstance(self._value, GenericServiceException):
            pass

class Right(ServiceDTO):
    def __init__(self, value):
        self._value = value
        super().__init__(value);
        
    def bind(self, func):
        return func(self._value)

class Left(ServiceDTO):
    def __init__(self, value):
        self._value = value
        
    def bind(self, func):
        return Left(self._value)


class GenericHttpData(BaseModel):
    message: str
    data: dict
    statusCode : int = 200



def ok(data:BaseModel | dict, msg: Optional[str]=None) -> ServiceDTO:
    if isinstance(data,dict):
        return Right(ServiceResult(message=msg or DEFAULT_SUCCESS_MSG
                                   ,data=data))
    return Right(ServiceResult(message=msg or DEFAULT_SUCCESS_MSG,data=data.model_dump()))

def err(msg: str,err_type: str,title:Enum = ErrorTitle.UNKNOWN) -> ServiceDTO:
    return Left(GenericServiceException(message=msg, errType=err_type,
                                        errTitle=str(title)))

def isRight(result : Either) -> bool:
    return isinstance(result, Right)

def isLeft(result : Either) -> bool:
    return isinstance(result, Left)

def runDomainService(domain_service : Callable, args, type_overwrite = AppErrors.VALIDATION):
    try:
        return domain_service(**args)
    except Exception as e:
        return err(type_overwrite, str(e), ErrorTitle.DOMAIN_ERROR)

# not yet use 
async def processDTOPacket(request: Request,call_next):
    response = await call_next(request)

    if not isinstance(response, ServiceDTO):
        return response

