from datetime import datetime
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel


class TodoPatcher(BaseModel):
    name: str | None = None
    topic: str | None = None
    description: str | None = None


class Todo(BaseModel):
    todoId: str
    name: str
    description: Optional[str]
    taskRefs: list[str]
    modifiedOn: float
    createdOn: float

    @classmethod
    def create(cls, name, description):
        tId = str(uuid4())
        tz = datetime.now().timestamp()

        return Todo(
            todoId=tId,
            name=name,
            description=description,
            taskRefs=[],
            createdOn=tz,
            modifiedOn=tz,
        )

    def add_task(self, taskId: str):
        if self.taskRefs.count(taskId) > 0:
            raise Exception("Cannot append the existing card in the reference")

        self.taskRefs.append(taskId)

    def remove_task(self, taskId: str):
        if self.taskRefs.count(taskId) == 0:
            raise Exception("Cannot delete non-existing card in the reference")

        self.taskRefs.remove(taskId)
