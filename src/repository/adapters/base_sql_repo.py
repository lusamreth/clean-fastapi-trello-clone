from contextlib import AbstractContextManager
from typing import Callable, Generic, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session
from typing_extensions import Any

from core.base_repo import BaseRepository

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


class LazyResult(Generic[T]):
    data: list[T]
    selected: Any

    def __init__(self, data, selected=None):
        self.data = data
        self.selected = selected


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

    def get(
        self, id: str, lazy_options: dict | None = None
    ) -> T | LazyResult | list[T] | None:
        with self.session_factory() as session:
            if lazy_options:
                res = (
                    session.query(self.model)
                    .filter(self.model.__dict__[self.identifier] == id)
                    .first()
                )

                if res is not None:
                    isQuery = lazy_options.get("query")
                    selector = (
                        lazy_options.get("queryField")
                        if isQuery is None
                        else isQuery.get("field")
                    )
                    queryList = res.__getattribute__(selector)

                    if isQuery is not None:
                        mapProp = isQuery.get("select")

                        mapKey = mapProp["field"]
                        mapFn = mapProp.get("mapFn")

                        if mapFn is not None:

                            def mapper(qRes) -> T:
                                val = qRes.__getattribute__(mapKey)
                                return mapFn(val)

                            mapped = map(
                                lambda queryResult: mapper(queryResult), queryList
                            )
                            return LazyResult(data=queryList, selected=list(mapped))

                        return LazyResult(
                            data=queryList,
                            selected=list(
                                map(lambda qRes: qRes.getattribute(mapKey), queryList)
                            ),
                        )
                        # return LazyResult()
                        # return list(mapped)

                    # if lazy_options["queryField"] == "boards":
                    #     print("QQ LIST", queryList, queryList[0].cards)

                    return queryList
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
