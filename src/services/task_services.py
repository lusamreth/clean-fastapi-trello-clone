from core.generics import err, ok, runDomainService, AppErrors
from domains.task import Task
from repository.protocols.task_repo_meta import TaskRepo
from repository.protocols.card_repo_meta import CardRepo

from schemas.task import (
    TaskResult,
    CreateTaskInput,
    FetchTaskResult,
    PatchTaskInput,
    PatchTaskOutput,
    RemoveTaskOutput,
)


def printNotFoundMsg(entityName: str, id: str):
    return "{} with id of {} is not Found!".format(entityName, id)


class TaskService:
    repo: TaskRepo
    cardRepo: CardRepo

    def __init__(self, repo: TaskRepo, cardRepo: CardRepo):
        self.repo = repo
        self.cardRepo = cardRepo

    def getAllTasks(self, taskId: str):
        tasks = self.cardRepo.get(taskId, lazy_options={"queryField": "tasks"})
        if tasks is None:
            return err(printNotFoundMsg("Board", taskId), AppErrors.EMPTY)

        convertor = lambda task: self.repo.db_to_entity(task)
        taskList = list(map(convertor, tasks))
        return ok(FetchTaskResult(cardList=taskList))

    # please implement lazy loading retrieval with the lazy = True option
    # in the base repo, because otherwise you will a problems loading
    # one-to-many relationship
    def createTask(self, task_data: CreateTaskInput):
        taskId = task_data.cardId
        task = self.cardRepo.get(taskId)
        if task is None:
            return err(printNotFoundMsg("Board", taskId), AppErrors.EMPTY)

        domainData = Task.create(name=task_data.name, description=task_data.content)
        _result = self.repo.add(**self.repo.entity_to_db(taskId, domainData, True))
        return ok(TaskResult(**domainData.model_dump()))

    def patchTask(self, taskId: str, task_data: PatchTaskInput):
        _res = self.repo.update(taskId, task_data)
        if _res is None:
            return err(printNotFoundMsg("Task", taskId), AppErrors.EMPTY)

        return ok(PatchTaskOutput(id=taskId, modified=_res, attributes=task_data))

    def deleteTask(self, taskId: str):
        _res = self.repo.remove(taskId)
        if _res is None:
            return err(printNotFoundMsg("Task", taskId), AppErrors.EMPTY)

        return ok(RemoveTaskOutput(id=taskId, removed=_res))
