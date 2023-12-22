from collections.abc import Callable
from fastapi import APIRouter, Depends, Path, Query, Response, Request
from typing import Annotated

from fastapi.routing import APIRoute

from api.v1.provider import getBoardService, getCardService, bearerSec

from schemas.card import (
    CreateCardInput,
    PatchCardInput,
)

from services.card_services import CardService


cardRouter = APIRouter(tags=["Card"])


@cardRouter.get("/many")
def getAllCards(
    board_id: str,
    cardService: CardService = Depends(getCardService),
):
    return cardService.getAllCards(board_id).unwrap()


@cardRouter.post("/")
def createCard(
    # board_id: str,
    card_data: CreateCardInput,
    cardService: CardService = Depends(getCardService),
):
    return cardService.createCard(card_data).unwrap()


@cardRouter.delete("/{card_id}")
def deleteCard(
    card_id: str,
    # board_id: str, delete_card: DeleteCardInput,
    cardService: CardService = Depends(getCardService),
):
    return cardService.deleteCard(card_id).unwrap()


@cardRouter.patch("/{card_id}")
def patchCard(
    card_id: str,
    card_patch: PatchCardInput,
    cardService: CardService = Depends(getCardService),
):
    return cardService.patchCard(card_id, card_patch).unwrap()
