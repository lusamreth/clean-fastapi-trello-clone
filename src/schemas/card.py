from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    topic: str
    content: str
    boardRef: str


class DeleteCardRequest(BaseModel):
    card_id: str
