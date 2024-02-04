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


def getResource(tag, resource=None):
    if resource is not None:
        return "{}/{}/{}".format(HOSTURL, tag, resource)
    else:
        return "{}/{}".format(HOSTURL, tag)


def serialize(json_payload: dict) -> ServiceResult:
    _cond1 = json_payload.get("data") is not None
    _cond2 = json_payload.get("message") is not None
    # rootLogger.info("json payload ", payload=json_payload)

    if _cond1 and _cond2:
        return ServiceResult(**json_payload)
    else:
        raise Exception("Bump Into error while serializing")


def makeAuthorizeServiceRequest(access_token: str):
    def authorizeRequest(
        method, url, data=None, params: dict = {}, **kwargs
    ) -> ServiceResult:
        _raw = rq.request(
            method=method,
            url=url,
            headers={"Authorization": "Bearer {}".format(access_token)},
            data=data,
            params=params,
            **kwargs,
        )

        # for some reason the request is created twice
        # intercept the status code to block this behavoir

        if _raw.status_code == 405:
            return ServiceResult(
                message="Method Not allowed", data={"type": "Not allowed"}
            )

        if _raw.status_code == 500:
            raise Exception(_raw.status_code)

        return serialize(_raw.json())

    return authorizeRequest


def makeAuthorizeRequest(access_token: str):
    def authorizeRequest(
        method, url, data=None, params: dict = {}, **kwargs
    ) -> ServiceResult:
        return rq.request(
            method=method,
            url=url,
            headers={"Authorization": "Bearer {}".format(access_token)},
            data=data,
            params=params,
            **kwargs,
        ).json()

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
    if jj.get("status") is None or jj.get("status") == 401:
        rootLogger.info("Already login!")
        rootLogger.info("Proceeding authentication...")

        login_res = rq.post(
            getResource("users", "login"),
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
        print(self.prevContext)
        print(self.prevContext[len(self.prevContext) - 1][fieldname])

        return self.prevContext[len(self.prevContext) - 1][fieldname]

    def extractPrimaryKey(self, queryStr: dict) -> str | None:
        for k in queryStr.keys():
            splt = k.split("_")

            if len(splt) == 2:
                val = queryStr[k]
                if splt[1] == "id":
                    return val

    # return self.

    def createIfEmpty(self, name, data, queryStr={}):
        rootLogger.info("LOGGED name {} {}".format(name, getResource(name)))
        singularName = name[:-1]
        identifier = singularName + "_" + "id"

        pk = (
            self.extractPrimaryKey(queryStr)
            if queryStr.get("isPrimaryKey") is True
            else None
        )

        RESOURCE_URL = getResource(name)

        if pk is not None:
            print("pKK", pk, identifier, queryStr)
            parentPlural = queryStr.get("parent") + "s"
            RESOURCE_URL = getResource(
                parentPlural,
                pk + "/" + name,
            )

        try:
            result = self.authReq("get", RESOURCE_URL)
        except Exception as e:
            rootLogger.error(str(e))
            exit(1)

        if result.data.get("type") is "Not allowed":
            return self

        if len(self.states) != 0:
            prev = self.states[-1]
            if prev is False:
                rootLogger.exception("Found failure! Cannot continue")

        rootLogger.info("fetch result of entity {} ".format(name), result=result)
        print(result)
        manyRes = result.data[name]
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
    authReq = makeAuthorizeServiceRequest(access_token=str(aToken))

    chainCaller = ChainCall(authReq)
    chainCaller.createIfEmpty(
        "cabinets",
        CreateCabinetInput(name="test", description="test").model_dump_json(),
    ).createIfEmpty(
        "boards",
        CreateBoardInput(
            cabinetId=chainCaller.tail("cabinetId"),
            name="test2",
            description="test2",
            topic="random",
        ).model_dump_json(),
        {
            "cabinet_id": chainCaller.tail("cabinetId"),
            "isPrimaryKey": True,
            "parent": "cabinet",
        },
    ).createIfEmpty(
        "cards",
        CreateCardInput(
            boardId=chainCaller.tail("boardId"),
            title="test2",
            content="test2",
        ).model_dump_json(),
        {
            "board_id": chainCaller.tail("boardId"),
            "isPrimaryKey": True,
            "parent": "board",
        },
    ).createIfEmpty(
        "todos",
        CreateTodoInput(
            cardId=chainCaller.tail("cardId"),
            name="test2",
            content="test2",
        ).model_dump_json(),
        {
            "card_id": chainCaller.tail("cardId"),
            "isPrimaryKey": True,
            "parent": "card",
        },
    )
    rootLogger.info("Parent daisy chaining test ran successfully!")


if __name__ == "__main__":
    main()
