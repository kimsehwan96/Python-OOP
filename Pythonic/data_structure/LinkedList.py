from abc import ABCMeta, abstractmethod
from node import SingleNode
from typing import Any


class LinkedList(metaclass=ABCMeta):
    def __init__(self):
        self._len = 0
        self._head = SingleNode()
        self._cursor = self._head

    @abstractmethod
    def append(self, data):
        raise NotImplementedError

    @abstractmethod
    def pop(self):
        raise NotImplementedError

    @abstractmethod
    def cur_value(self) -> Any:
        raise NotImplementedError

    def __len__(self):
        return self._len
