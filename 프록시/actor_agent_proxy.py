class Actor:
    def __init__(self) -> None:
        self.is_busy = False

    def occupied(self) -> None:
        self.is_busy = True
        print(type(self).__name__, "은/는 다른영화를 촬영중입니다.")

    def available(self) -> None:
        self.is_busy = False
        print(type(self).__name__, "은/는 촬영 가능합니다.")

    def get_status(self) -> bool:
        return self.is_busy


class Agent:
    def __init__(self) -> None:
        self.actor = Actor()
        self.principal = None

    def work(self):
        if self.actor.get_status():
            self.actor.occupied()
        else:
            self.actor.available()


if __name__ == '__main__':
    r = Agent()
    r.work()
    r.actor.occupied()
    r.work()