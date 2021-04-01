from typing import Any
from abc import ABCMeta, abstractmethod


class BaseNode(metaclass=ABCMeta):
    def __init__(self):
        self._next = None
        self._data = None

    @abstractmethod
    def data(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def data(self, data) -> Any:
        raise NotImplementedError

    @abstractmethod
    def next(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def next(self, node):
        raise NotImplementedError


class SingleNode(BaseNode):

    @property
    def next(self) -> BaseNode:
        return self._next

    @next.setter
    def next(self, node: BaseNode) -> None:
        if not isinstance(node, BaseNode):
            raise TypeError("parameter must be a node")
        self._next = node

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, data: Any) -> None:
        self._data = data


class DoubleNode(SingleNode):
    def __init__(self) -> None:
        super().__init__()
        self._prev = None

    @property
    def prev(self) -> BaseNode:
        return self._prev

    @prev.setter
    def prev(self, node: BaseNode) -> None:
        if not isinstance(node, BaseNode):
            raise TypeError("parameter must be a node")
        self._prev = node


if __name__ == '__main__':
    n1 = SingleNode()
    n2 = SingleNode()
    d = DoubleNode()

    d.prev = n1
    d.next = n2

    print(d.prev)
    print(d.next)
