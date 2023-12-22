from abc import abstractmethod
from core.base_repo import BaseRepository
from domains.task import Task
from repository.model.todo import TaskSchema


class TaskRepo(BaseRepository):
    def db_to_entity(self, todo_repo_data: TaskSchema | None) -> Task | None:
        pass

    @abstractmethod
    def entity_to_db(
        self, board_id: str, todo_schema_data: Task | None, to_dict: bool
    ) -> TaskSchema | dict | None:
        pass
