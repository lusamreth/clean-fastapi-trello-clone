from abc import abstractmethod

from core.base_repo import BaseRepository
from domains.todo import Todo, TodoPatcher
from repository.model.todo import TodoSchema


class TodoRepo(BaseRepository[TodoSchema]):
    @abstractmethod
    def db_to_entity(
        self,
        todo_repo_data: TodoSchema | None,
        tasksRef: list[str] = [],
        to_dict: bool = False,
    ) -> Todo | None:
        pass

    @abstractmethod
    def entity_to_db(
        self,
        board_id: str,
        todo_schema_data: Todo | None,
        to_dict: bool,
    ) -> TodoSchema | dict | None:
        pass

    @abstractmethod
    def update(self, todo_id: str, patch_todo: TodoPatcher) -> TodoSchema | None:
        pass
