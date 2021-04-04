from LinkedList import LinkedList
from node import SingleNode
from exceptions import EmptyLinkedListPopError


class SingLinkedList(LinkedList):
    def __init__(self):
        super().__init__()
        self._cur_value = None

    def __iter__(self):
        pass

    def append(self, data):
        if self._len == 0:
            self._cursor.data = data
            self._len += 1
            self.cur_value = data
        else:
            self._cursor.next = SingleNode()
            self._cursor = self._cursor.next
            self._cursor.data = data
            self._len += 1
            self.cur_value = data

    def pop(self):
        if self._len == 0:
            raise EmptyLinkedListPopError
        else:
            pass
        # 아.. 전 노드를 어떻게 알아내지? 뇌정지상태임
        # 뇌사코드 작성중.. 내일 다시함

    @property
    def cur_value(self):
        return self._cursor.data

    @cur_value.setter
    def cur_value(self, data):
        self._cur_value = data


if __name__ == '__main__':
    l = SingLinkedList()
    l.append(1)
    l.append(2)
    print(l.cur_value)
    print(len(l))

# TODO: implement above methods !!
