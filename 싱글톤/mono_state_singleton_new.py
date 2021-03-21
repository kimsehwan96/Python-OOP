class Foo:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Foo, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj


if __name__ == '__main__':
    f = Foo()
    f1 = Foo()

    f.x = 4

    print("Foo object f : ", f)
    print("Foo object f1 : ", f1)
    # f와 f1은 다른 객체이다.
    print("f's attribute x :", f.x)
    print("f1's attribute x :", f1.x)
    # 하지만 상태를 공유한다!

"""
output
Foo object f :  <__main__.Foo object at 0x7fd8e00c4640>
Foo object f1 :  <__main__.Foo object at 0x7fd8e00c4760>
f's attribute x : 4
f1's attribute x : 4
"""