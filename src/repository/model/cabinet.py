from sqlalchemy import DateTime, ForeignKey, String
from database.main import Base
from sqlalchemy.sql import func

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
    cabinet = relationship("CabinetSchema", back_populates="boards")


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
    created_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
