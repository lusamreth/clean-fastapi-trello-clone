from core.generics import AppErrors, err, ok, runDomainService
from domains.todo import Todo
from repository.adapters.base_sql_repo import LazyResult
from repository.protocols.card_repo_meta import CardRepo
from repository.protocols.todo_repo_meta import TodoRepo
from schemas.todo import (
    CreateTodoInput,
    FetchTodoResult,
    PatchTodoInput,
    PatchTodoOutput,
    RemoveTodoOutput,
    TodoResult,
)


def printNotFoundMsg(entityName: str, id: str):
    return "{} with id of {} is not Found!".format(entityName, id)


class TodoService:
    repo: TodoRepo
    cardRepo: CardRepo

    def __init__(self, repo: TodoRepo, cardRepo: CardRepo):
        self.repo = repo
        self.cardRepo = cardRepo

    def getAllTodos(self, todoId: str):
        todoLazyResult = self.cardRepo.get(
            todoId,
            lazy_options={
                "query": {
                    "field": "todos",
                    "select": {
                        "field": "tasks",
                        "mapFn": lambda tasks: list(
                            map(lambda task: task.task_id, tasks)
                        ),
                    },
                }
            },
        )

        if todoLazyResult is None:
            return err(printNotFoundMsg("Board", todoId), AppErrors.EMPTY)

        if not isinstance(todoLazyResult, LazyResult):
            return err("Board repo yeild incorrect lazy result", AppErrors.INTERNAL)

        def convertor(todo_tuple):
            index, todo = todo_tuple
            entity = self.repo.db_to_entity(todo, todoLazyResult.selected[index])
            if entity is None:
                return err(printNotFoundMsg("Todo", todoId), AppErrors.EMPTY)
            return TodoResult(**entity.model_dump())

        # convertor = lambda todo: self.repo.db_to_entity(todo,convertor)
        todoList = list(map(convertor, enumerate(todoLazyResult.data)))
        return ok(FetchTodoResult(todos=todoList))

    # please implement lazy loading retrieval with the lazy = True option
    # in the base repo, because otherwise you will a problems loading
    # one-to-many relationship
    def createTodo(self, todo_data: CreateTodoInput):
        todoId = todo_data.cardId
        todo = self.cardRepo.get(todoId)
        if todo is None:
            return err(printNotFoundMsg("Board", todoId), AppErrors.EMPTY)

        domainData = Todo.create(name=todo_data.name, description=todo_data.content)
        self.repo.add(**self.repo.entity_to_db(todoId, domainData, True))
        return ok(TodoResult(**domainData.model_dump()))

    def patchTodo(self, todoId: str, todo_data: PatchTodoInput):
        _res = self.repo.update(todoId, todo_data)
        if _res is None:
            return err(printNotFoundMsg("Todo", todoId), AppErrors.EMPTY)

        return ok(PatchTodoOutput(id=todoId, modified=_res, attributes=todo_data))

    def deleteTodo(self, todoId: str):
        _res = self.repo.remove(todoId)
        if _res is None:
            return err(printNotFoundMsg("Todo", todoId), AppErrors.EMPTY)

        return ok(RemoveTodoOutput(id=todoId, removed=_res))
