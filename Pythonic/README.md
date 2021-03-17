# 파이써닉한 코드

## 자체 시퀀스 생성

- `__getitem__`이라는 매직 메서드를 통해 작동.
- 시퀀스는 `__getitem__`과 `__len__`을 모두 구현하는 객체이므로 반복이 가능
- 리스트, 퓨플, 문자열은 표준 라이브러리에 있는 시퀀스 객체의 예다.

- 클래스가 표준 라이브러리 객체를 감싸는 래퍼인 경우 기본 객체에 가능한 많은 동작을 위임 할 수 있다. 즉 클래스가 리스트의 래퍼인 경우 리스트의 동일한 메서드를 호출하여 호환성을 유지 가능
- 다음은 리스트를 wrapping하는 예이다.

```python3
class Items:
    def __init__(self, *values):
        self._values = list(values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item):
        return self._values.__getitem__(item)


if __name__ == '__main__':
    items = Items(1,2,3,4,5,6,7,8)
    print(len(items))
    print(items[0]) # 1
    print(items[1]) # 2

```

## 래퍼도 아니고 내장 객체도 아닌 자신만의 시퀀스 구현

- 다음 사항을 유의 할 것

1. 범위로 인덱싱하는 결과가 해당 클래스와 같은 타입의 인스턴스여야 한다.
2. slice에 의해 제공된 범위는 파이썬이 하는 것 처럼 마지막 요소는 제외해야 한다.

## 커스텀 시퀀스 구현 예시

```python3
class Foo:
    def __init__(self):
        self.bar = list()

    def add(self, item):
        self.bar.append(item)

    def remove(self, index):
        self.bar.pop(index)

    def __str__(self):
        return str(self.bar)

    def __contains__(self, item):
        """
        매직메서드, 멤버십 테스트에 이용된다.
        """
        return item in self.bar

    def __iter__(self):
        return iter(item for item in self.bar)

    def __getitem__(self, index):
        return self.bar[index]

    def __setitem__(self, key, value):
        self.bar[key] = value

    def __delitem__(self, key):
        del self.bar[key]

    def __len__(self):
        return len(self.bar)

if __name__ == "__main__":
    f = Foo()
    f.add(1)
    f.add(2)
    print(f)
    f[0] = 100
    print(100 in f)
    print(len(f))
```

- 여기서 배운 점

`__foo__` 와 같이 앞뒤에 언더바 2개가 붙은 메서드들을 매직메서드라고 부르는데.. 

단순한 메서드가 아닌 특수한 기능을 하는 메서드라는 것을 오늘 깨달았다.

`__len__` 매직 메서드의 경우, 구현을 해놓으면, `class.__len__()` 와 같이 호출하는게 아니라
`len(class)` 와 같이 호출 할 수 있더라 !

`__str__` 매직 메서드의 경우, 클래스 자체를 출력하고자 할 때, 해당 클래스에 `class.__str__`와 같이 해당 매직메서드가 구현되어있으면
`print(class)`를 하였을때 해당 매직메서드가 수행된다. 이 메서드는 무조건 문자열을 리턴해야 한다.

일반적인 메서드와 호출되는 방식이 다르다고 보면 될듯

## 컨텍스트 관리자

간단히 말해서 `with` 구문을 말하는 것.

파일 디스크립터는 열고 난 뒤에 작업을 마무리하는 시점에 닫아주어야 한다.

고전적인 파이썬 코드는 다음과 같이 코딩 될 것이다.

```python3
fd = open(filename, 'r')
# do something!
fd.close()
# close file descriptor
```

하지만 파이써닉하게 컨텍스트 관리자를 활용하여 다음과 같이 수정 가능

```python3
with open(filename, 'r') as f:
    # do something!
```

- 대부분 파일 디스크립터의 열고 닫는 이슈에서 활용하는데. 위 기능을 따져본다면 DB 커넥션 관리에도 활용 가능하다.
- 컨텍스트 관리자는 `__enter__` 와 `__exit__` 매직 메서드로 구현된다.

## 커스텀 클래스를 매직메서드를 활용해서 컨텍스트 매니저 구현 !

```python3
def stop_database():
    print('stop')


def start_database():
    print('start')


class DBHandler(object):
    """
    DB가 오프라인 상태에서만 작업하기 위한 DB 핸들러
    """

    def __enter__(self):
        stop_database()
        return self  # 굳이 반환값이 없어도 되지만, 웬만하면 객체 자신을 리턴해주는 것으로 구현하자 !

    def __exit__(self, exc_type, exc_val, exc_tb):
        start_database()  # 컨텍스트 관리자를 탈출한 이후에 DB를 스타트


def db_backup():
    print("db backup start")


if __name__ == "__main__":
    with DBHandler():
        db_backup()

```

출력

```console
/usr/local/bin/python3.8 /Users/gimsehwan/PycharmProjects/Python-OOP/Pythonic/custom_context_manager.py
stop
db backup start
start
```