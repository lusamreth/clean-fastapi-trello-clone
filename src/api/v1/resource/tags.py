from enum import Enum


class RouterTag(str, Enum):
    BOARD = "board"
    CABINET = "cabinet"
    CARD = "card"
    TODO = "todo"
    AUTH = "auth"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value).capitalize()
