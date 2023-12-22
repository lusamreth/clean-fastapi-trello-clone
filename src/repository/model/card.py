from sqlalchemy import DateTime, ForeignKey, String
from database.main import Base
from sqlalchemy.sql import func
from .todo import TodoSchema
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)


class CardSchema(Base):
    __tablename__: str = "card"
    card_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1028), nullable=True)
    todos: Mapped[list["TodoSchema"]] = relationship(
        cascade="all,delete", uselist=True, lazy=True
    )
    board_id: Mapped[str] = mapped_column(ForeignKey("board.board_id"))
    created_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    modified_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
