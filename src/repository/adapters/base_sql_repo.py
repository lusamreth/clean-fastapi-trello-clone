from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.base_repo import BaseRepository
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class BaseRepo(BaseRepository[T]):
    def __init__(
        self,
        session_factory: Callable[
            ..., AbstractContextManager[Session]
        ],
        model,
    ) -> None:
        self.session_factory = session_factory
        self.model = model

    def add(self, **schema):
        query = self.model(**schema)
        with self.session_factory() as session:
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as error:
                raise Exception(
                    "Duplicate key found\nDetail: {}".format(error)
                )

        return query

    def update(self, id, patches):
        with self.session_factory() as session:
            session.query(self.model).filter(
                self.model.id == id
            ).update(patches.dict())
            session.commit()

    def get(self, id: str):
        return
        pass

    def list(self, id: str):
        return
        pass

    def remove(self, id):
        with self.session_factory() as session:
            query = (
                session.query(self.model)
                .filter(self.model.id == id)
                .first()
            )
            session.delete(query)
            session.commit()


# BaseRepo()
