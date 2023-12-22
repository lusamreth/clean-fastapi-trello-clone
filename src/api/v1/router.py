from fastapi import FastAPI
from .endpoints.cabinet_route import cabinetRouter
from .endpoints.user_route import userRouter
from .endpoints.auth_router import authRouter
from .endpoints.board_router import boardRouter
from .endpoints.card_router import cardRouter
from .endpoints.todo_router import todoRouter


authPrefix = "/auth"
userPrefix = "/user"
cabinetPrefix = "/cabinet"
boardPrefix = "/board"
cardPrefix = "/card"
todoPrefix = "/todo"


def initializeRouter(app: FastAPI):
    app.include_router(userRouter, prefix=userPrefix)
    app.include_router(cabinetRouter, prefix=cabinetPrefix)
    app.include_router(authRouter, prefix=authPrefix)
    app.include_router(boardRouter, prefix=boardPrefix)
    app.include_router(cardRouter, prefix=cardPrefix)
    app.include_router(todoRouter, prefix=todoPrefix)
