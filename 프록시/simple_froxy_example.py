class SubjectInterface:
    def add(self, a, b):
        pass

    def sub(self, a, b):
        pass


class RealSubject(SubjectInterface):
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b


class ProxyClass(SubjectInterface):
    def __init__(self):
        self.subject = RealSubject()

    def add(self, a, b):
        return self.subject.add(a, b)

    def sub(self, a, b):
        return self.subject.sub(a, b)


if __name__ == "__main__":
    p = ProxyClass()
    print(p.add(100, 25))
    print(p.sub(100, 25))