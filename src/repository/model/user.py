from sqlalchemy import Integer, String
from database.main import Base
from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    Mapped,
)


class UserSchema(Base):
    __tablename__: str = "user"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))


#  UserSchema.__table__.create(bind=sql_engine, checkfirst=True)
# AutoCreateTable(UserSchema)
