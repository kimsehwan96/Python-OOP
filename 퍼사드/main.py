from event_manager import EventManager


class You:
    def __init__(self):
        print('행사 준비를 시작합니다')

    def ask_event_manager(self):
        print('이벤트 매니저에게 위임합니다.')

        em = EventManager()
        em.arrange()

    def __del__(self):
        print('You 클래스의 인스턴스가 사라집니다. 이벤트 매니저 역시 같이 사라집니다.')


if __name__ == '__main__':
    you = You()
    you.ask_event_manager()
