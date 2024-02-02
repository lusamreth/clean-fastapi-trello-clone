import logging
import logging.config
import os
import sys
from datetime import datetime

import structlog
from pydantic import BaseModel
from rich.json import JSON
from rich.logging import RichHandler
from rich.text import Text

from src.configs.settings import getSettings

settings = getSettings()

logPath = "./logs/tests"


def createLogPath():
    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
        if not os.path.isdir(logPath):
            os.mkdir(logPath)
    return logPath


class TestLogger:
    logDir: str
    logHandlersConfig: dict
    logHandlers: list[str]

    def __init__(self, logName: str, logDir: str, logLevel=logging.NOTSET):
        self.foreignLogChain = [
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.stdlib.ExtraAdder(),
        ]

        def set_process_id(_, __, event_dict):
            event_dict["process_id"] = os.getpid()
            return event_dict

        self.processors = [
            structlog.threadlocal.merge_threadlocal_context,
            structlog.contextvars.merge_contextvars,
            *self.foreignLogChain,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        self.logDir = logDir
        self.loadLogDictCfg()

        structlog.configure(
            processors=self.processors,
            wrapper_class=structlog.make_filtering_bound_logger(logLevel),
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
        )

        # self.rootLogger = logging.getLogger(logName)
        # self.structLogger = structlog.get_logger(logName)
        self.rootLogger = structlog.get_logger(logName)

    def timeBasedLogFile(self):
        loggedTime = datetime.now().today()
        timeFormat = "{}".format(
            loggedTime.isoformat(),
        )
        filenameFormat = "{}/test-{}.log".format(
            self.logDir,
            timeFormat,
        )
        return filenameFormat

    # this can only be called at the end of the format processors
    def structLogToRichTextProcessor(self, logger, method_name, event_dict: dict):
        strFormat = "[bold blue][[ {} ]] [yellow]{}".format(
            event_dict["timestamp"], event_dict["event"]
        )

        richText = Text(strFormat)
        excludeFields = ["timestamp", "event", "level"]

        for event_key in event_dict.keys():
            _value = event_dict.get(event_key)
            if event_key in excludeFields:
                continue

            if isinstance(_value, dict):
                # strFormat += JSON.from_data(_value)
                richText.append("[bold red] [JSON] \n", style="bold magenta")
                jsonTxt = JSON.from_data(_value).text
                richText.append_text(jsonTxt)
                richText.append("\n")
                richText.append("\n")
                # richText.append(JSON.from_data(_value).text)
            elif isinstance(_value, str):
                richText.append(Text("[{} : [red]{}] ".format(event_key, _value)))
                pass
            else:
                pass

        richText.append("\n")
        return richText

    def setThreadInfo(self, logger, method_name, event_dict):
        """
        Extract thread and process names and add them to the event dict.
        """
        if type(event_dict) == str:
            return event_dict

        # print("eventtt", event_dict, method_name, logger)
        record = event_dict["_record"]
        result = event_dict.get("result")
        if record is None:
            return event_dict

        if result is not None and isinstance(result, BaseModel):
            event_dict["result"] = result.dict()

        event_dict["thread_name"] = record.threadName
        event_dict["process_name"] = record.processName

        return event_dict

    def loadLogDictCfg(self):
        logDict = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": self.getFormatterConfig(),
            "handlers": self.configureHandlers(),
            "loggers": {
                "": {
                    "handlers": ["file", "default"],
                    "level": logging.NOTSET,
                    "propagate": True,
                },
            },
        }

        logging.config.dictConfig(logDict)

    #     Ri
    # lambda: RichPicologgingHandler(markup=True, rich_tracebacks=True)
    def getFormatterConfig(self):
        formatters = {
            # "rich": {"format": "%(name)s - %(message)s"},
            "standard": {
                "format": "%(levelname)s - %(asctime)s - %(name)s - %(module)s - %(message)s"
            },
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    # self.extractFromEventRecord,
                    self.setThreadInfo,
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.TimeStamper(
                        fmt="%Y-%m-%d %H:%M:%S", utc=False
                    ),
                    self.structLogToRichTextProcessor,
                ],
                "foreign_pre_chain": self.foreignLogChain,
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    # self.extractFromEventRecord,
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.JSONRenderer(sort_keys=True),
                ],
                "foreign_pre_chain": self.foreignLogChain,
            },
        }
        return formatters

    def configureHandlers(self):
        logHandlers = {
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": self.timeBasedLogFile(),
                "formatter": "json",
            },
            "default": {
                # "class": "logging.StreamHandler",
                # "()": self.customizeRichHandler,
                "class": "rich.logging.RichHandler",
                "markup": True,
                "rich_tracebacks": True,
                "level": "DEBUG",
                "formatter": "colored",
            },
        }

        return logHandlers

    @classmethod
    def getLogger(cls, log_name, log_dir, level=logging.NOTSET):
        return cls(log_name, log_dir, level).rootLogger
