from sqlalchemy import DateTime, ForeignKey, String
from database.main import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)


class TodoSchema(Base):
    __tablename__: str = "todo"
    todo_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    card_id: Mapped[str] = mapped_column(ForeignKey("card.card_id"))
    name: Mapped[str] = mapped_column(String(255))
    modified_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    # card = relationship("CardSchema", back_populates="todos")
    tasks: Mapped[list["TaskSchema"]] = relationship("TaskSchema", lazy=True)


class TaskSchema(Base):
    __tablename__: str = "task"
    task_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    description: Mapped[str] = mapped_column(String(255))
    todo_id: Mapped[str] = mapped_column(ForeignKey("todo.todo_id"))
    created_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    status: Mapped[str] = mapped_column(String(255))
    assigned_to: Mapped[str] = mapped_column(String(255))
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    modified_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    due_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
