from pydantic import BaseModel


class GenericHttpData(BaseModel):
    message: str
    data: dict
