from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic, Optional, TypeVar


class ContextManagerRepository(ABC):
    @abstractmethod
    def commit(self):
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.commit()


T = TypeVar("T")


class BaseReadOnlyRepository(
    Generic[T],
    ABC,
):
    @abstractmethod
    def get(self, id: str) -> Optional[T]:
        ...

    @abstractmethod
    async def list(self) -> Iterable[T]:
        ...


# ContextManagerRepository
class BaseWriteOnlyRepository(Generic[T], ABC):
    @abstractmethod
    def add(self, detail: T) -> T:
        ...

    @abstractmethod
    def remove(self, id: str) -> bool:
        ...


class BaseRepository(
    BaseReadOnlyRepository[Generic[T]],
    BaseWriteOnlyRepository[Generic[T]],
    ABC,
):
    ...
