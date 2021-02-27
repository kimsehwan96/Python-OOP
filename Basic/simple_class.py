class Message:
    version = "1.0"  # 클래스 속성, 모든 인스턴스가 공유하는 attribute

    def __init__(self, content=""):  # __init__ magic method. 생성자. 인스턴스별로 다른 속성들을 정의하는게 보편적인 use case
        self.content = content

    def __str__(self):  # 인스턴스를 그냥 호출했을 때 콘솔에서 보일 내용을 정의함.
        return f'message content : {self.content}'

    def __del__(self):
        print("this message will be deleted from memory")
        del self

    def send(self, target=None) -> bool:  # 사실 이런 메서드들은 정적 메서드로 구현하는것이 더 올바른 방식임.
        if target is None:
            print('you should put where you want to send message')
            return False
        if type(target) != (list or tuple):
            print(f'send msg successfully target : {target}')
        else:
            for v in target:
                print(f'send msg successfully target : {v}')
        return True


if __name__ == '__main__':
    msg = Message("안녕하세요")
    print(msg) # message content : 안녕하세요
    targets = ['kim', 'lee', 'park']
    msg.send(targets)

    #참조가 끝난 이후에 알아서 __del__ 메서드가 수행됨
    #최종 아웃풋

    '''
    message content : 안녕하세요
    send msg successfully target : kim
    send msg successfully target : lee
    send msg successfully target : park
    this message will be deleted from memory
    '''
