from contextlib import AbstractContextManager
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.exc import IntegrityError
from core.base_repo import BaseRepository
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


def clearNone(original: dict):
    filtered = {k: v for k, v in original.items() if v is not None}
    original.clear()
    original.update(filtered)
    return filtered


class LazyOption:
    def __init__(self, queryField, lazy_type="select"):
        self.queryField = queryField
        self.lazy_type = lazy_type


class BaseRepo(BaseRepository[T]):
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        model,
        primary_key_identifier="id",
    ) -> None:
        self.session_factory = session_factory
        self.model = model
        self.identifier = primary_key_identifier
        self.auto_model_conversion = False

    def add(self, **schema):
        query = self.model(**schema)
        # if self.auto_model_conversion:
        #     query = schema
        with self.session_factory() as session:
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as error:
                raise Exception("Duplicate key found\nDetail: {}".format(error))

        return query

    def update(self, id, patches) -> int:
        if isinstance(patches, dict):
            filteredPatches = clearNone(patches)
        else:
            filteredPatches = clearNone(patches.dict())

        with self.session_factory() as session:
            update_status = (
                session.query(self.model)
                .filter(self.model.__dict__[self.identifier] == id)
                .update(filteredPatches)
            )

            session.commit()
            return update_status

    def get(self, id: str, lazy_options: dict | None = None) -> T | None:
        with self.session_factory() as session:
            if lazy_options:
                res = (
                    session.query(self.model)
                    .filter(self.model.__dict__[self.identifier] == id)
                    .first()
                )
                if res is not None:
                    return res.__getattribute__(lazy_options["queryField"])
            else:
                res = (
                    session.query(self.model)
                    .filter(self.model.__dict__[self.identifier] == id)
                    .first()
                )
                return res

    def list(self, id: str):
        raise NotImplemented()

    def remove(self, id):
        with self.session_factory() as session:
            query = (
                session.query(self.model)
                .filter(self.model.__dict__[self.identifier] == id)
                .first()
            )
            if query is None:
                return None

            _isDel = session.delete(query)
            session.commit()
            return True


# BaseRepo()
