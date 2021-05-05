class Subject:
    def __init__(self):
        self.__observers = []

    def register(self, observer):
        self.__observers.append(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer:
    def __init__(self, subject, name: str):
        self._name = name
        subject.register(self)

    def notify(self, subject, *args, **kwargs):
        print(f'{self._name} got args: {args}, kwargs: {kwargs} from {subject}')


if __name__ == '__main__':
    subject = Subject()
    ob1 = Observer(subject, 'ob1')
    ob2 = Observer(subject, 'ob2')

    subject.notify_all('notification!', keyword='value')


"""
result:
ob1 got args: ('notification!',), kwargs: {'keyword': 'value'} from <__main__.Subject object at 0x7fa3c88c1950>
ob2 got args: ('notification!',), kwargs: {'keyword': 'value'} from <__main__.Subject object at 0x7fa3c88c1950>
"""