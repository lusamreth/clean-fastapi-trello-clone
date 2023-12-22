from core.utils.helpers import unwrapEntityTimeSet
from domains.task import Task, TaskPatcher
from repository.model.todo import TaskSchema
from ..adapters.base_sql_repo import BaseRepo
from ..protocols.task_repo_meta import TaskRepo


class TaskRepoImpl(BaseRepo[TaskSchema], TaskRepo):
    def __init__(self, session_factory):
        super().__init__(
            model=TaskSchema,
            session_factory=session_factory,
            primary_key_identifier="task_id",
        )

    def db_to_entity(
        self,
        db_model: TaskSchema | None,
        to_dict: bool = True,
    ) -> Task | dict | None:
        # def dbmTodoConvertor(todo: TodoSchema) -> Todo:
        #     pass

        # taskId: str
        # description: str
        # dueDate: Optional[float]
        # assignedTo: Optional[str]
        # status: TaskStatus
        # modifiedOn: float
        # createdOn: float

        if db_model is not None:
            dbm = db_model
            param = {
                "taskId": dbm.task_id,
                "dueDate": float(dbm.due_date.timestamp()),
                "description": dbm.title,
                "assignedTo": dbm.assigned_to,
                "status": dbm.status,
                # "createdOn": float(dbm.created_on.timestamp()),
                **unwrapEntityTimeSet(dbm).model_dump(),
            }
            if to_dict:
                return param
            else:
                return Task(**param)

    def entity_to_db(
        self, todo_id: str, entity: Task | None, to_dict=False
    ) -> TaskSchema | dict | None:
        if entity is not None:
            param = {
                "task_id": entity.taskId,
                "due_date": entity.dueDate,
                "description": entity.description,
                "todo_id": todo_id,
                "assigned_to": entity.assignedTo,
                "status": entity.status,
                **unwrapEntityTimeSet(entity).model_dump(),
            }

            if to_dict:
                return param
            else:
                return TaskSchema(**param)
