from abc import ABC
from src.core.base_repo import (
    BaseReadOnlyRepository,
    BaseRepository,
)
import pydantic
import unittest


class SampleEntity(pydantic.BaseModel):
    id: str


class SampleRepo(BaseRepository, ABC):
    def __init__(self) -> None:
        self.data: list[SampleEntity] = [SampleEntity(id="burh")]

    def get(self, id: str):
        return list(filter(lambda _x: _x.id == id, self.data)).pop()

    def list(self):
        return self.data

    def add(self, data: SampleEntity):
        self.data.append(data)

    def remove(self):
        return SampleEntity(id="burh")

    def update(self):
        return SampleEntity(id="burh")


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.entity = SampleEntity(id="1")
        self.repo = SampleRepo()

    def testGet(self):
        print(self.repo.get("burh"))

    def testAdd(self):
        self.repo.add(self.entity)
        print(self.repo.list())


if __name__ == "__main__":
    unittest.main()
