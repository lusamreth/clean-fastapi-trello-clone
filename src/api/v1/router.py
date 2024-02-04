from fastapi import FastAPI

from .endpoints.auth_router import authRouter
from .endpoints.board_router import boardRouter, boardSharedRouter
from .endpoints.cabinet_route import cabinetRouter
from .endpoints.card_router import cardRouter, cardSharedRouter
from .endpoints.todo_router import todoRouter, todoSharedRouter
from .endpoints.user_route import userRouter
from .resource.prefixes import RouterPrefix

# authPrefix = "/auth"
# userPrefix = "/users"
# cabinetPrefix = "/cabinets"
# boardPrefix = "/boards"
# cardPrefix = "/cards"
# todoPrefix = "/todos"


def initializeRouter(app: FastAPI):
    app.include_router(userRouter, prefix=RouterPrefix.USER)
    app.include_router(authRouter, prefix=RouterPrefix.AUTH)

    app.include_router(cabinetRouter, prefix=RouterPrefix.CABINET)
    app.include_router(boardSharedRouter, prefix=RouterPrefix.CABINET)

    app.include_router(boardRouter, prefix=RouterPrefix.BOARD)
    app.include_router(cardSharedRouter, prefix=RouterPrefix.BOARD)

    app.include_router(cardRouter, prefix=RouterPrefix.CARD)
    app.include_router(todoSharedRouter, prefix=RouterPrefix.CARD)

    app.include_router(todoRouter, prefix=RouterPrefix.TODO)
