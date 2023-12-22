from collections.abc import Callable
from enum import Enum
from typing import Generic, Optional, TypeVar

from fastapi import Request
from oslash import Either
from pydantic import BaseModel

from core.constants import AppErrors, ErrorTitle
from core.exceptions import (
    AuthError,
    DuplicatedError,
    InternalError,
    NotFoundError,
    ValidationError,
)

DEFAULT_SUCCESS_MSG = "Request successfully fullfilled"

from enum import Enum


class ServiceResult(BaseModel):
    message: str
    data: dict


class GenericServiceException(BaseModel):
    message: str
    errType: str
    errTitle: str


class BaseBinaryResult(Either[ServiceResult, GenericServiceException]):
    def __init__(self, value: ServiceResult | GenericServiceException):
        self._value = value


class ErrorDTOFactory:
    def __init__(self):
        self._DTO_Map = {}

    def registerErrorType(self, type_name: str, err_class_init):
        self._DTO_Map[type_name] = err_class_init

    def create(self, key, **kwargs):
        builder = self._DTO_Map.get(key)
        if not builder:
            raise ValueError("Error with type <{}> is not yet registered.".format(key))
        return builder(**kwargs)

    def fromServiceToWeb(self, wrapped_value: BaseBinaryResult):
        if not isinstance(wrapped_value, BaseBinaryResult):
            return wrapped_value

        value = wrapped_value._value

        if isRight(wrapped_value) and isinstance(value, ServiceResult):
            # self._value.message.
            return value
        elif isLeft(wrapped_value) and isinstance(value, GenericServiceException):
            eType = value.errType
            createErrObjFunc = self.create(
                eType, message=value.message, title=value.errTitle
            )
            raise createErrObjFunc
        else:
            return wrapped_value


# DTO TYPE SETTINGS
DTO2HttpFactory = ErrorDTOFactory()

DTO2HttpFactory.registerErrorType(AppErrors.AUTH, AuthError.create)
DTO2HttpFactory.registerErrorType(AppErrors.VALIDATION, ValidationError.create)
DTO2HttpFactory.registerErrorType(AppErrors.EMPTY, NotFoundError.create)
DTO2HttpFactory.registerErrorType(AppErrors.INTERNAL, InternalError.create)
# DTO2HttpFactory.registerErrorType(AppErrors., NotFoundError.create)


class ServiceDTO(BaseBinaryResult):
    def __init__(self, value: ServiceResult | GenericServiceException):
        super().__init__(value)

    def unwrap(self):
        if isinstance(self._value, ServiceResult):
            return self._value
        elif isinstance(self._value, GenericServiceException):
            return DTO2HttpFactory.fromServiceToWeb(self)

    def unwrap_or(self, _alternative):
        if isinstance(self._value, ServiceResult):
            return self._value
        else:
            return _alternative

    def handleSuccess(self):
        pass

    def handleFailure(self):
        pass


class Right(ServiceDTO):
    def __init__(self, value):
        self._value = value
        super().__init__(value)

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
    statusCode: int = 200


def ok(data: BaseModel | dict, msg: Optional[str] = None) -> ServiceDTO:
    if not isinstance(data, BaseModel):
        return Right(ServiceResult(message=msg or DEFAULT_SUCCESS_MSG, data=data))

    return Right(
        ServiceResult(message=msg or DEFAULT_SUCCESS_MSG, data=data.model_dump())
    )


def err(msg: str, err_type: str, title: Enum = ErrorTitle.UNKNOWN) -> ServiceDTO:
    return Left(
        GenericServiceException(message=msg, errType=err_type, errTitle=str(title))
    )


def isRight(result: Either) -> bool:
    return isinstance(result, Right)


def isLeft(result: Either) -> bool:
    return isinstance(result, Left)


def runDomainService(
    domain_service: Callable, args=None, type_overwrite=AppErrors.VALIDATION
):
    try:
        return domain_service()
    except Exception as e:
        # raise Exception(err(type_overwrite, str(e), ErrorTitle.DOMAIN_ERROR))
        return err(type_overwrite, str(e), ErrorTitle.DOMAIN_ERROR)


# not yet use
async def processDTOPacket(request: Request, call_next):
    response = await call_next(request)

    if isinstance(response, ServiceDTO):
        return response
    else:
        return response
