from sqlalchemy import BigInteger, Integer, String
from database.main import Base
from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    Mapped,
)


class TokenSchema(Base):
    __tablename__: str = "auth"
    jti: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255))
    token_value: Mapped[str] = mapped_column(String(1025))
    token_type: Mapped[str] = mapped_column(String(255))
    expire_at: Mapped[int] = mapped_column(Integer)


#  UserSchema.__table__.create(bind=sql_engine, checkfirst=True)
# AutoCreateTable(UserSchema)sqlachemy
