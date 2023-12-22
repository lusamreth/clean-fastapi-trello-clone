from pydantic import BaseModel
from domains.card import Card, CardPatcher
from .base_crud import (
    CreateActionInput,
    PatchActionOutput,
    FetchActionBulks,
    RemoveActionOutput,
)


class CreateCardInput(BaseModel):
    title: str
    content: str
    boardId: str


class DeleteCardInput(BaseModel):
    cardId: str


class FetchCardBulksInput(FetchActionBulks):
    cardId: str


class CardResult(Card):
    pass


class FetchCardResult(BaseModel):
    cards: list[CardResult]


class PatchCardInput(CardPatcher):
    pass


class RemoveCardOutput(RemoveActionOutput):
    pass


class PatchCardOutput(PatchActionOutput):
    attributes: CardPatcher
