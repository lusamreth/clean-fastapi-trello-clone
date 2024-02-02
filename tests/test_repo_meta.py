import json
import unittest
from abc import ABC
from collections.abc import Iterable
from datetime import datetime
from typing import Optional

import pydantic

from src.core.base_repo import BaseRepository


class SampleEntity(pydantic.BaseModel):
    id: str
    name: str
    createdAt: float
    modifiedAt: float

    @classmethod
    def create(cls, id, name) -> "SampleEntity":
        nowTime = datetime.now().timestamp()
        return cls(id=id, name=name, createdAt=nowTime, modifiedAt=nowTime)


class SampleEntityPatches(pydantic.BaseModel):
    name: str | None


class SampleRepo(BaseRepository, ABC):
    def __init__(self) -> None:
        nowTime = datetime.now().timestamp()
        self.data_in_memory: list[SampleEntity] = [
            SampleEntity(
                name="sample-001", id="test-001", createdAt=nowTime, modifiedAt=nowTime
            )
        ]

    def get(self, id: str, lazy_options: dict | None = None) -> Optional[SampleEntity]:
        if lazy_options is not None and lazy_options["mode"] == "lazy":
            nowTime = datetime.now().timestamp()
            return SampleEntity(
                name="sample-001", id="test-001", createdAt=nowTime, modifiedAt=nowTime
            )

        filtered = list(filter(lambda _x: _x.id == id, self.data_in_memory))
        return filtered.pop() if len(filtered) > 0 else None

    def list(self) -> Iterable[SampleEntity]:
        return self.data_in_memory

    def add(self, data: SampleEntity) -> SampleEntity:
        self.data_in_memory.append(data)
        return data

    def remove(self, id: str) -> bool:
        for i, data in enumerate(self.data_in_memory):
            if data.id == id:
                self.data_in_memory.pop(i)
                return True

        return False

    def update(self, sample_id: str, data: SampleEntityPatches) -> SampleEntity:
        _exist = self.get(sample_id)
        if _exist is None:
            raise Exception("Sample entity is not found")
        return SampleEntity(*_exist.dict, **data.dict())


class SampleFileRepo(BaseRepository[SampleEntity], ABC):
    def __init__(self):
        self.data_file_name = "data.json"
        self.sample = SampleEntity.create("test-001", "sample-001")
        # initial dump of the data
        with open(self.data_file_name, "w") as file:
            json.dump(
                {"test-data": [self.sample.model_dump()]},
                file,
            )

    def get(self, id: str, lazy_options: dict | None = None) -> Optional[SampleEntity]:
        with open(self.data_file_name, "r") as f:
            _data = json.load(f)
            sample_data = _data["test-data"]
            for _, data in enumerate(sample_data):
                if data.get("id") == id:
                    return SampleEntity(**data)
        pass

    def list(self) -> Iterable[SampleEntity]:
        with open(self.data_file_name, "r") as f:
            _data = json.load(f)
            return _data

    def add(self, data: SampleEntity) -> SampleEntity:
        with open(self.data_file_name, "r") as f:
            _data = json.load(f)
            _data["test-data"].append(data.model_dump())

        with open(self.data_file_name, "w") as writtable:
            json.dump(_data, writtable)

        return data

    def remove(self, id: str) -> bool:
        _tag_deleted = False
        with open(self.data_file_name, "r") as f:
            _data = json.load(f)
            sample_data = _data["test-data"]
            for i, data in enumerate(sample_data):
                if data.get("id") == id:
                    sample_data.pop(i)
                    _data["test-data"] = sample_data
                    writtable = open(self.data_file_name, "w")
                    json.dump(_data, writtable)
                    writtable.close()

                    return True

        return _tag_deleted

    def update(
        self, sample_id: str, patchData: SampleEntityPatches
    ) -> SampleEntity | None:
        modified_sample = None

        with open(self.data_file_name, "r+") as f:
            _data = json.load(f)
            sample_data = _data["test-data"]

            for i, data in enumerate(sample_data):
                print("Dta", data, id, data.get(id), data.get("id"))
                if data.get("id") == sample_id:
                    old_state = sample_data.pop(i)

                    try:
                        _ = SampleEntity(**old_state)
                        modified_content = {
                            **old_state,
                            **patchData.model_dump(),
                            "modifiedAt": datetime.now().timestamp(),
                        }
                        # print("modfl", modified_content)
                        modified_sample = SampleEntity(**modified_content)

                    except Exception as e:
                        raise ValueError("Invalid sample data found!")

                    sample_data.append(modified_sample.model_dump())
                    _data["test-data"] = sample_data

                    writtable = open(self.data_file_name, "w")
                    json.dump(_data, writtable)
                    writtable.close()

        return modified_sample


class TestMemoryRepo(unittest.TestCase):
    def setUp(
        self,
    ):
        self.firstSampleId = "test-001"
        self.secondSample = SampleEntity.create(id="test-002", name="sample-002")

        self.repo = SampleRepo()

    def testGet(self):
        _non_exist = self.repo.get("test-003")
        self.assertTrue(_non_exist is None)

        _exist = self.repo.get(self.firstSampleId)
        self.assertTrue(_exist is not None)

    def testAdd(self):
        self.repo.add(self.secondSample)
        self.assertTrue(
            self.repo.list(), [self.repo.get(self.firstSampleId), self.secondSample]
        )


class TestFileRepo(unittest.TestCase):
    def setUp(
        self,
    ):
        self.firstSampleId = "test-001"
        self.secondSample = SampleEntity.create(id="test-002", name="sample-002")

        self.repo = SampleFileRepo()

    def testAdd(self):
        self.repo.add(self.secondSample)

        with open(self.repo.data_file_name, "r+") as f:
            _data = json.load(f)
            self.assertTrue(_data["test-data"][1]["name"], self.secondSample.name)
            self.assertEqual(len(_data["test-data"]), 2)

    def testRemove(self):
        # self.repo.add(self.secondSample)
        _remove_res = self.repo.remove(self.firstSampleId)
        self.assertTrue(_remove_res)

        with open(self.repo.data_file_name, "r") as f:
            _data = json.load(f)
            self.assertEqual(len(_data["test-data"]), 0)

    def testList(self):
        self.assertTrue(self.repo.list(), [self.firstSampleId, self.secondSample])

    def testGet(self):
        getRes = self.repo.get(self.firstSampleId)
        self.assertTrue(getRes is not None)

    def testUpdate(self):
        self.repo.update(self.firstSampleId, SampleEntityPatches(name="sample-00X"))
        result = self.repo.get(self.firstSampleId)

        print(result)
        self.assertTrue(result is not None)

        assert result is not None
        self.assertEqual(result.name, "sample-00X")

    pass


if __name__ == "__main__":
    unittest.main()
