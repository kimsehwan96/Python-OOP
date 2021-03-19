class Singleton(object):
    __instance = None

    def __init__(self):
        if not Singleton.__instance:
            print("객체가 아직 없음 !")
        else:
            print("객체가 이미 생성되어있음 !", self.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Singleton()
        return cls.__instance


if __name__ == "__main__":
    s = Singleton()  # 클래스를 초기화는 했지만.. 객체를 생성하진 않았다.
    print("객체 생성!", Singleton.get_instance())
    s1 = Singleton()
