from functools import lru_cache
from core.security import JWTBearer
from database.main import Database
from repository.adapters.auth_repo import AuthRepoImpl
from repository.adapters.board_repo import BoardRepoImpl
from repository.adapters.cabinet_repo import CabinetRepoImpl
from repository.adapters.todo_repo import TodoRepoImpl
from repository.adapters.user_repo import UserRepoImpl
from repository.adapters.card_repo import CardRepoImpl

from services.auth_services import AuthService
from services.board_services import BoardService
from services.card_services import CardService
from services.todo_services import TodoService
from services.user_services import UserService
from services.cabinet_services import CabinetService


db_container = Database()
session = db_container.getSession()
bearerSec = JWTBearer()

authImpl = AuthRepoImpl(session)
userImpl = UserRepoImpl(session)
cabinetImpl = CabinetRepoImpl(session)
boardImpl = BoardRepoImpl(session)
cardImpl = CardRepoImpl(session)
todoImpl = TodoRepoImpl(session)


userService = UserService(repo=userImpl, authRepo=authImpl)
authService = AuthService(repo=authImpl)
cabinetService = CabinetService(repo=cabinetImpl)
boardService = BoardService(repo=boardImpl, parentService=cabinetService)
cardService = CardService(repo=cardImpl, boardRepo=boardImpl)
todoService = TodoService(repo=todoImpl, cardRepo=cardImpl)


@lru_cache
def getUserService():
    return userService


@lru_cache
def getAuthService():
    return authService


@lru_cache
def getCabinetService():
    return cabinetService


@lru_cache
def getBoardService():
    return boardService


@lru_cache
def getCardService():
    return cardService


@lru_cache
def getTodoService():
    return todoService
