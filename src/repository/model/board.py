from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.main import Base

from .cabinet import CabinetSchema
from .card import CardSchema


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
        # back_populates="board",
        uselist=True,
        lazy="select"
        # lazy="subquery",
    )
    cabinet = relationship("CabinetSchema", back_populates="boards")
