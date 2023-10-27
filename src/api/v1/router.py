from fastapi import FastAPI
from .endpoints.cabinet_route import cabinetRouter
from .endpoints.user_route import userRouter
from .endpoints.auth_router import authRouter


authPrefix = "/auth"
userPrefix = "/user"
cabinetPrefix = "/cabinet"

def initializeRouter(app: FastAPI):
    app.include_router(userRouter,prefix=userPrefix)
    app.include_router(cabinetRouter,prefix=cabinetPrefix)
    app.include_router(authRouter,prefix=authPrefix)

