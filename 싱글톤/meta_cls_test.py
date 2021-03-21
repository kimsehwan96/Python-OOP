class MyInt(type):
    """
    커스텀 Int 클래스. __call__ 매직메서드는 객체가 초기화 될때 수행할 메서드임.
    """

    def __call__(cls, *args, **kwargs):
        print("-- 내가 정의한 int 클래스 -- ", args)
        return type.__call__(cls, *args, **kwargs)


class int(metaclass=MyInt):
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    i = int(4, 5)

"""
output
-- 내가 정의한 int 클래스 --  (4, 5)
"""