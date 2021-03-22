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

## 프로퍼티, 속성과 객체 메서드의 다른 타입들

public, private, protected 등 프로퍼티를 가지는 다른 언어와는 다르게 파이썬의 모든 객체와 함수는
public이다. 즉 호출자가 객체의 속성을 호출하지 못하도록 할 방법이 없다 !

엄격한 강제사항은 없지만 몇가지 규칙이 있다. 밑줄로 시작하는 속성은 해당 객체에 대해 private을 의미하며.
외부에서 호출하지 않기로 기대하는 것이다. 다시 말해서 금지하진 않은 것!

### 파이썬에서의 밑줄

```python3
class Connector:
    def __init__(self, source):
        self.source = source
        self._timeout = 60

conn = Connector('postgresql://localhost:1234')
conn.source # 'postgresql://localhost:1234'
conn._timeout # 60

conn.__dict__  # {'source': 'postgresql://localhost:1234', '_timeout': 60}
```

여기서 Connector 객체는 source로 생성되며, source와 timeout 두개의 속성을 가진다.

우리는 timeout 객체를 private으로 쓰기를 기대하지만. 강제는 불가능하다.
따라서 conn._timeout 을 통해 객체의 속성을 접근하고, 변경하는것이 가능하다. (하진 말아야 겠지만..)

**여기서 알고 갈 점**

객체는 외부 호출 객체와 관련된 속성과 메서드만을 노출해야 한다.  즉 객체의 인터페이스를 공개하는 용도가 아니라면
모든 멤버에는 접두사로 하나의 밑줄을 사용하는것이 좋다. 

이런 규칙을 준수하면 리팩토링 할 때, 객체의 인터페이스를 유지하면서 리팩토링이 가능해서 사이드이펙트 걱정이 줄어든다.

나도 매우 크게 오해하고 있었던 점중 하나는. 언더바 두개를 쓰면 해당 속성을 외부에서 접근 할 경우 attribute exception이 발생해서
나는 private을 구현한거구나 라고 생각했다. 하지만 매우 큰 오산 !

```python3
class Connector:
    def __init__(self, source):
        self.source = source
        self.__timeout = 60

conn = Connector('postgresql://localhost:1234')
conn.source # 'postgresql://localhost:1234'
conn.__timeout # AttributeError: 'Connector' object has no attribute '__timeout'

conn.__dict__  # {'source': 'postgresql://localhost:1234', '_Connector__timeout': 60}

# __timeout 이라는 속성이 없을 뿐이지. 실제로는 _Connector__timeout 이라는 속성으로 존재한다 !

conn._Connector__timeout # 60
```

위 코드를 보면 주석으로 내가 정리해놓았다. 

더블언더바를 사용해서 속성을 정의하는 것은. private이 아니다! 위에서 보듯이 `_{className}__{attributename}`로 이름이 변경되는데
이를 이름 맹글링(name mangling)이라고 한다. 

위에서 `conn.__timeout`을 접근할 경우 `AttributeError`가 발생한것은. 속성의 이름이 변경되어서 발생한것이지. private이여서가 아니다!

더블언더바의 경우 여러번 확장되는 클래스에 대해서 메서드 이름 충돌을 피하기 쉽게 해주기 위해서 만들어 진것이지, 
private으로 쓰라고 만든것이 아니다.

그러니까 위 예제처럼 쓰면 파이써닉한 코드와는 거리가 멀어지는 것.

따라서 private의 개념은 언더바 하나를 사용해서 코드를 작성하는 습관을 들이도록 하자!