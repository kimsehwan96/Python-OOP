# Set을 이용한 옵저버 패턴

class Subscriber(object):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print("{0}, {1}".format(self.name, message))


class Publisher(object):
    def __init__(self):
        self.subscribers = set()

    def register(self, who):
        self.subscribers.add(who)

    def unregister(self, who):
        self.subscribers.discard(who)

    def dispatch(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)


if __name__ == '__main__':
    pub = Publisher()
    a = Subscriber('a')
    b = Subscriber('b')
    c = Subscriber('c')

    pub.register(a)
    pub.register(b)
    pub.register(c)

    pub.dispatch("점심시간입니다.")
    pub.unregister(b)
    pub.dispatch("저녁시간입니다.")
