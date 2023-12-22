import json
import logging
import os
import random
from datetime import datetime, time
from pathlib import Path

import requests as rq
from structlog import configure, get_logger
from structlog.stdlib import LoggerFactory

from core.generics import GenericServiceException, ServiceResult
from src.configs.settings import getSettings
from src.schemas.board import CreateBoardInput
from src.schemas.cabinet import CreateCabinetInput
from src.schemas.card import CreateCardInput
from src.schemas.todo import CreateTodoInput
from src.schemas.user import LoginInfoInput, RegistrationInfoInput

# from src.schemas. import CreateBoardInput


settings = getSettings()

logPath = "./logs/tests"


def createLogPath():
    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
        if not os.path.isdir(logPath):
            os.mkdir(logPath)


createLogPath()
import structlog

loggedTime = datetime.now().today()
timeFormat = "{}:{}-{}".format(loggedTime.minute, loggedTime.hour, loggedTime.date())
filenameFormat = "{}/{}-run".format(
    logPath,
    timeFormat,
)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        # structlog.processors.JSONRenderer(),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(
        file=Path(filenameFormat).with_suffix(".log").open("wt")
    ),
    # logger_factory=structlog.PrintLoggerFactory(),
    # cache_logger_on_first_use=False,
)

rootLogger = get_logger()

# rootLogger = logging.getLogger()
# rootLogger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
loggedTime = datetime.now().today()

timeFormat = "{}:{}-{}".format(loggedTime.minute, loggedTime.hour, loggedTime.date())
filenameFormat = "{}/{}-run".format(
    logPath,
    timeFormat,
)


# HOSTURL = "http://{}:{}".format(settings.HOST, settings.PORT)
HOSTURL = "http://{}:{}".format("0.0.0.0", "8000")
API_VERSION = "v1"

# log = rootLogger.Logger("liveTestLogger")


def getResource(tag, resource=""):
    return "{}/{}/{}".format(HOSTURL, tag, resource)


def serialize(json_payload: dict) -> ServiceResult:
    _cond1 = json_payload.get("data") is not None
    _cond2 = json_payload.get("message") is not None
    logging.debug("json payload: {}".format(json_payload))

    if _cond1 and _cond2:
        return ServiceResult(**json_payload)
    else:
        print(json_payload)
        raise Exception("Bump Into error while serializing")


def makeAuthorizeRequest(access_token: str):
    def authorizeRequest(method, url, data=None, **kwargs) -> ServiceResult:
        _raw = rq.request(
            method=method,
            url=url,
            headers={"Authorization": "Bearer {}".format(access_token)},
            data=data,
            **kwargs
        ).json()
        return serialize(_raw)

    return authorizeRequest


def authProcess() -> ServiceResult:
    registration_res = rq.post(
        getResource("user", "register"),
        data=RegistrationInfoInput(
            username="test",
            email="test@gmail.com",
            password1="test@123456789",
            password2="test@123456789",
        ).model_dump_json(),
    )

    jj = registration_res.json()
    if jj.get("status") is None or jj.get("status") == 403:
        rootLogger.info("Already login!")
        rootLogger.info("Proceeding authentication...")

        login_res = rq.post(
            getResource("user", "login"),
            data=LoginInfoInput(
                email="test@gmail.com",
                password="test@123456789",
            ).model_dump_json(),
        )

        rootLogger.info("login res: {}".format(login_res.json()))
        return serialize(login_res.json())
    else:
        raise Exception("Cannot handling this status code {}".format(jj["status"]))


class ChainCall:
    def __init__(self, authReq):
        self.authReq = authReq
        self.states = []
        self.prevContext = []

    def tail(self, fieldname: str, level=-1) -> str:
        print(self.prevContext[len(self.prevContext) - 1][fieldname])
        return self.prevContext[len(self.prevContext) - 1][fieldname]

    def createIfEmpty(self, name, data, queryStr={}):
        try:
            result = self.authReq("get", getResource(name, "many"), params=queryStr)
        except Exception as e:
            rootLogger.error(str(e))
            exit(1)

        if len(self.states) != 0:
            prev = self.states[-1]
            if prev is False:
                print("Found failure! Cannot continue")

        pluralName = "{}s".format(name)

        rootLogger.info("Fetch Result of {} : {}".format(name, result))

        manyRes = result.data[pluralName]
        if len(manyRes) == 0:
            postRes = self.authReq("post", getResource(name), data)
            # print("postRes", postRes)
            self.prevContext.append(postRes.data)
            isValid = postRes.data is not None
            self.states.append(isValid)
        else:
            if len(manyRes) > 0:
                self.prevContext.append(manyRes.pop())

        return self


def main():
    aRes = authProcess()
    aToken = aRes.data["accessToken"] if authProcess is not None else ""
    authReq = makeAuthorizeRequest(access_token=str(aToken))
    chainCaller = ChainCall(authReq)
    chainCaller.createIfEmpty(
        "cabinet",
        CreateCabinetInput(name="test", description="test").model_dump_json(),
    ).createIfEmpty(
        "board",
        CreateBoardInput(
            cabinetId=chainCaller.tail("cabinetId"),
            name="test2",
            description="test2",
            topic="random",
        ).model_dump_json(),
        {"cabinet_id": chainCaller.tail("cabinetId")},
    ).createIfEmpty(
        "card",
        CreateCardInput(
            boardId=chainCaller.tail("boardId"),
            title="test2",
            content="test2",
        ).model_dump_json(),
        {"board_id": chainCaller.tail("boardId")},
    )


if __name__ == "__main__":
    main()
    pass
