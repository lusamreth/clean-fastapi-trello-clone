from typing import Optional
from pydantic_core.core_schema import NullableSchema
from sqlalchemy import DateTime, String
from database.main import Base
from sqlalchemy.sql import func
from .user import UserSchema

from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)

class BoardSchema(Base):
    __tablename__: str = "board"
    board_id : Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))


class CabinetSchema(Base):
    __tablename__: str = "cabinet"
    cabinet_id: Mapped[str] = mapped_column(
        String(255), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    board_id_refs : Mapped[list["BoardSchema"]] = relationship(back_populates="cabinetSchema",uselist=True)
    created_on :  Mapped[DateTime] = mapped_column(DateTime(timezone=True),default=func.now())
    
