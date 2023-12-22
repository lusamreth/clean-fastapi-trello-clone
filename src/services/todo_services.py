from core.generics import err, ok, runDomainService, AppErrors
from domains.todo import Todo
from repository.protocols.todo_repo_meta import TodoRepo
from repository.protocols.card_repo_meta import CardRepo

from schemas.todo import (
    TodoResult,
    CreateTodoInput,
    FetchTodoResult,
    PatchTodoInput,
    PatchTodoOutput,
    RemoveTodoOutput,
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
        todos = self.cardRepo.get(todoId, lazy_options={"queryField": "todos"})
        if todos is None:
            return err(printNotFoundMsg("Board", todoId), AppErrors.EMPTY)

        convertor = lambda todo: self.repo.db_to_entity(todo)
        todoList = list(map(convertor, todos))
        return ok(FetchTodoResult(cardList=todoList))

    # please implement lazy loading retrieval with the lazy = True option
    # in the base repo, because otherwise you will a problems loading
    # one-to-many relationship
    def createTodo(self, todo_data: CreateTodoInput):
        todoId = todo_data.cardId
        todo = self.cardRepo.get(todoId)
        if todo is None:
            return err(printNotFoundMsg("Board", todoId), AppErrors.EMPTY)

        domainData = Todo.create(name=todo_data.name, description=todo_data.content)
        _result = self.repo.add(**self.repo.entity_to_db(todoId, domainData, True))
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
