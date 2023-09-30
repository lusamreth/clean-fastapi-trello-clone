from abc import ABCMeta
from abc import abstractmethod


class BaseService(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
