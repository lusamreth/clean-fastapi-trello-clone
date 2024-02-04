from datetime import datetime
from functools import wraps

from pydantic import BaseModel, ConfigDict
from sqlalchemy.types import DateTime


def exceptionHandler(args):
    args_inner = args

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(args, kwargs)

        return wrapper

    return decorator


class TimeSet(BaseModel):
    modifiedOn: float
    createdOn: float
    model_config = ConfigDict(arbitrary_types_allowed=True)


class DBTimeSet(BaseModel):
    modified_on: datetime
    created_on: datetime
    model_config = ConfigDict(arbitrary_types_allowed=True)


def unwrapEntityTimeSet(timeset: TimeSet) -> DBTimeSet:
    return DBTimeSet(
        modified_on=datetime.fromtimestamp(timeset.modifiedOn),
        created_on=datetime.fromtimestamp(timeset.createdOn),
    )


def unwrapDBTimeSet(db_data: DBTimeSet) -> TimeSet:
    return TimeSet(
        createdOn=float(db_data.created_on.timestamp()),
        modifiedOn=float(db_data.modified_on.timestamp()),
    )
