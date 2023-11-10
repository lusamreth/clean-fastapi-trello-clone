from contextlib import AbstractContextManager
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.exc import IntegrityError
from core.base_repo import BaseRepository
from typing import Callable, Generic, TypeVar
import inspect

T = TypeVar("T")


def clearNone(original: dict):
    filtered = {k: v for k, v in original.items() if v is not None}
    original.clear()
    original.update(filtered)
    return filtered


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

    def update(self, id, patches):
        if isinstance(patches, dict):
            filteredPatches = clearNone(patches)
        else:
            filteredPatches = clearNone(patches.dict())
        with self.session_factory() as session:
            session.query(self.model).filter(
                self.model.__dict__[self.identifier] == id
            ).update(filteredPatches)
            session.commit()

    def get(self, id: str) -> T | None:
        with self.session_factory() as session:
            res = (
                session.query(self.model)
                .filter(self.model.__dict__[self.identifier] == id)
                .one()
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
                raise Exception("Element Not found!")

            isDel = session.delete(query)
            session.commit()
            return isDel


# BaseRepo()
