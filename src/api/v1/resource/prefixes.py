from enum import Enum


class RouterPrefix(str, Enum):
    BOARD = "/boards"
    CABINET = "/cabinets"
    CARD = "/cards"
    TODO = "/todos"
    AUTH = "/auth"
    USER = "/users"

    def __str__(self) -> str:
        return str(self.value)


# authPrefix = "/auth"
# userPrefix = "/users"
# cabinetPrefix = "/cabinets"
# boardPrefix = "/boards"
# cardPrefix = "/cards"
# todoPrefix = "/todos"
