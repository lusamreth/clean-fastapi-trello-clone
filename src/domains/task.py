from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4


class TaskPatcher(BaseModel):
    description: str | None = None
    isCompleted: Optional[bool]


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    DELETED = "deleted"


class Task(BaseModel):
    taskId: str
    description: str
    dueDate: Optional[float]
    assignedTo: Optional[str]
    status: TaskStatus
    modifiedOn: float
    createdOn: float

    @classmethod
    def create(cls, description: str) -> "Task":
        tId = str(uuid4())
        tz = datetime.now().timestamp()

        return Task(
            taskId=tId,
            description=description,
            createdOn=tz,
            dueDate=None,
            status=TaskStatus.PENDING,
            assignedTo=None,
            modifiedOn=tz,
        )

    def markedSoftDelete(self):
        self.status = TaskStatus.DELETED

    def assignTo(self, user_id: str):
        self.assignedTo = user_id

    def toggleComplete(self):
        isCompleted = self.status == TaskStatus.COMPLETED
        if not isCompleted:
            self.status = TaskStatus.COMPLETED
        else:
            self.status = TaskStatus.PENDING
