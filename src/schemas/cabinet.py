from pydantic import BaseModel


class PostCabinet(BaseModel):
    cabinet_name: str
    description: str
