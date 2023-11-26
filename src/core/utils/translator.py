from pydantic import ValidationError
from core.generics import AppErrors, ServiceDTO,ServiceResult,GenericServiceException, isLeft, isRight

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

        if not isinstance(wrapped_value,ServiceDTO):
            return wrapped_value

        value = wrapped_value._value

        if isRight(wrapped_value) and isinstance(value,ServiceResult):
            return value
        elif isLeft(wrapped_value) and isinstance(value,GenericServiceException):
            eType = value.errType;
            createErrObjFunc = self.create(eType, 
                                   message=value.message,
                                   title=value.errTitle);
            raise createErrObjFunc
        else:
            return wrapped_value


# async def processDTOPacket(request: Request,call_next):
#     response = await call_next(request)
#     return DTO2HttpFactory.fromServiceToWeb(response)
