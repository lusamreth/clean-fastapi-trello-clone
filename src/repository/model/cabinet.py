from sqlalchemy import DateTime, Float, ForeignKey, String
from database.main import Base
from sqlalchemy.sql import func
from .card import CardSchema
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)


class BoardSchema(Base):
    __tablename__: str = "board"
    board_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1028), nullable=True)
    topic: Mapped[str] = mapped_column(String(255))
    cabinet_id: Mapped[str] = mapped_column(
        ForeignKey("cabinet.cabinet_id", ondelete="CASCADE")
    )
    cards: Mapped[list["CardSchema"]] = relationship(
        cascade="all,delete",
        backref="board",
        uselist=True,
        lazy=True,
        # lazy="joined",
    )
    cabinet = relationship("CabinetSchema", back_populates="boards")
    modified_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))


class CabinetSchema(Base):
    __tablename__: str = "cabinet"
    cabinet_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1028), nullable=True)
    # board_id_refs : Mapped[list["BoardSchema"]] = relationship(back_populates="cabinetSchema",uselist=True)
    boards: Mapped[list["BoardSchema"]] = relationship(
        cascade="all,delete", back_populates="cabinet", uselist=True, lazy="subquery"
    )

    modified_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    created_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
