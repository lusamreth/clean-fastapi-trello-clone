from sqlalchemy import String
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    DeclarativeBase,
    relationship,
)
from sqlalchemy.orm.properties import ForeignKey


class Base(DeclarativeBase):
    def __init__(self):
        pass


class Author(Base):
    __tablename__ = "author"
    id: Mapped[str] = mapped_column(primary_key=True, default=None)
    name: Mapped[str] = mapped_column(String(30))
    board_ref: Mapped[list["Cabinet"]] = relationship(
        back_populates="board_ref"
    )


class Cabinet(Base):
    __tablename__ = "cabinet"
    id: Mapped[str] = mapped_column(primary_key=True, default=None)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))
    author: Mapped["Author"] = relationship(back_populates="author")
    board: Mapped[list["Board"]] = relationship(
        back_populates="cards"
    )


class Board(Base):
    __tablename__ = "board"
    id: Mapped[str] = mapped_column(primary_key=True, default=None)
    name: Mapped[str] = mapped_column(String(30))
    cabinet_id: Mapped[str] = mapped_column(ForeignKey("cabinet.id"))
    cabinet: Mapped["Cabinet"] = relationship(back_populates="board")
    topic: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))
    cards: Mapped[list["Card"]] = relationship(
        back_populates="board"
    )


class Card(Base):
    __tablename__ = "card"
    text: Mapped[str] = mapped_column(String())
    id: Mapped[str] = mapped_column(primary_key=True, default=None)
    board_id: Mapped[str] = mapped_column(ForeignKey("board.id"))
