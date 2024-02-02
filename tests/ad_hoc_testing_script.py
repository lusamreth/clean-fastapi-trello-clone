import json
import logging
import logging.config
import os
import sys
from datetime import datetime

import requests as rq
import structlog

from core.generics import GenericServiceException, ServiceResult
from core.logger.logger_test import TestLogger
from src.configs.settings import getSettings
from src.schemas.board import CreateBoardInput
from src.schemas.cabinet import CreateCabinetInput
from src.schemas.card import CreateCardInput
from src.schemas.todo import CreateTodoInput
from src.schemas.user import LoginInfoInput, RegistrationInfoInput

settings = getSettings()

logPath = "./logs/tests"


def createLogPath():
    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
        if not os.path.isdir(logPath):
            os.mkdir(logPath)
    return logPath


rootLogger = TestLogger.getLogger("ad-hoc-test-logger", createLogPath())

HOSTURL = "http://{}:{}".format("0.0.0.0", "8000")
API_VERSION = "v1"


def getResource(tag, resource=""):
    return "{}/{}/{}".format(HOSTURL, tag, resource)


def serialize(json_payload: dict) -> ServiceResult:
    _cond1 = json_payload.get("data") is not None
    _cond2 = json_payload.get("message") is not None
    rootLogger.info("json payload ", payload=json_payload, extra={"markup": True})

    if _cond1 and _cond2:
        return ServiceResult(**json_payload)
    else:
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
        rootLogger.info("login response ", result=login_res.json())
        return serialize(login_res.json())
    else:
        raise Exception("Cannot handling this status code {}".format(jj["status"]))


class ChainCall:
    def __init__(self, authReq):
        self.authReq = authReq
        self.states = []
        self.prevContext = []

    def tail(self, fieldname: str, level=-1) -> str:
        # print(self.prevContext[len(self.prevContext) - 1][fieldname])
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
                rootLogger.exception("Found failure! Cannot continue")

        pluralName = "{}s".format(name)
        rootLogger.info("fetch result of entity {} ".format(name), result=result)

        manyRes = result.data[pluralName]
        if len(manyRes) == 0:
            postRes = self.authReq("post", getResource(name), data)
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
