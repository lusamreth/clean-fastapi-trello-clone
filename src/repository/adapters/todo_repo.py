from core.utils.helpers import unwrapDBTimeSet
from domains.todo import Todo, TodoPatcher
from repository.model.todo import TodoSchema
from ..adapters.base_sql_repo import BaseRepo
from ..protocols.todo_repo_meta import TodoRepo


class TodoRepoImpl(BaseRepo[TodoSchema], TodoRepo):
    def __init__(self, session_factory):
        super().__init__(
            model=TodoSchema,
            session_factory=session_factory,
            primary_key_identifier="card_id",
        )

    def db_to_entity(
        self, db_model: TodoSchema | None, to_dict: bool = True
    ) -> Todo | dict | None:
        # def dbmTodoConvertor(todo: TodoSchema) -> Todo:
        #     pass
        if db_model is not None:
            dbm = db_model
            param = {
                "cardId": dbm.card_id,
                "description": dbm.title,
                # todoRefs=dbm.todos,
                "todoRefs": dbm.todos,
                **unwrapDBTimeSet(dbm).model_dump(),
                # "createdOn": float(dbm.created_on.timestamp()),
                # "modifiedOn": float(dbm.modified_on.timestamp()),
            }
            if to_dict:
                return param
            else:
                return Todo(**param)

    def entity_to_db(
        self, board_id: str, entity: Todo | None, to_dict=False
    ) -> TodoSchema | dict | None:
        if entity is not None:
            param = {
                "todo_id": entity.todoId,
                "todos": entity.taskRefs,
                "description": entity.description,
                "board_id": board_id,
                **unwrapDBTimeSet(entity).model_dump(),
            }

            if to_dict:
                return param
            else:
                return TodoSchema(**param)
