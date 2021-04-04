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

## 프로퍼티

객체에 값을 저장해야 할 경우 어트리뷰트를 사용 할 수 있다. 때로는 객체의 상태나 다른 속성의 값을
기반으로 어떤 계산을 하려고 할 때도 있다. 이런 경우 대부분 프로퍼티를 사용하는 것이 좋은 선택이다.

프로퍼티는 객체의 어떤 속성에 대해 접근을 제어하려는 경우 사용한다. 이렇게 하는것도 파이써닉 한거다!

자바나 다른 프로그래밍 언어에서는 접근 메서드 (게터/세터)를 만들지만, 파이썬에서는 프로퍼티를 쓸 것

사용자가 등록한 정보에 잘못된 정보가 입력되지 않게 보호하려고 한다고 생각하자.
아래 코드는 프로퍼티를 사용해 접근을 제한하고, 유효성을 체크하는 파이썬 코드다!

```python3
import re

EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+[^@]+")


def is_valid_email(potentially_valid_email: str):
    return re.match(EMAIL_FORMAT, potentially_valid_email) is not None


class User:
    def __init__(self, username):
        self.username = username
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not is_valid_email(new_email):
            raise ValueError("유효한 이메일이 아닙니다.")
        self._email = new_email


if __name__ == '__main__':
    u1 = User('kim')
    # u1.email = 'kim@'  # ValueError
    u1.email = 'kim@kim.com'
    print(u1.email)

```

여기서 주의할점

1. 나는 `@property.setter` 라고 실수했었는데, 그게 아니라 `@property`로 정의한 속성을
`setter`앞에 붙여주어야 한다. `@email.setter` 와 같이 말이다.

2. 대부분의 경우에는 일반 속성을 사용해도 무방하다. 다만 속성의 값을 통해 연산하거나, 유성 체크를 할 경우에 프로퍼티로
만들어서 사용하는게 효과적이다!
   
또한 위 예제에서 착안 할 수 있는점은 한 메서드에서 한 가지 이상의 일을 하지 말라는 것.
무언가를 할당하고, 유효성 체크를 하고 싶다면 두개 이상의 문장(statement)로 나눠라!

## 이터러블 객체

파이썬에는 기본적으로 반복 가능한 객체가 있다. 예를 들어 리스트, 튜플, 세트 및 사전은 원하는 구조의 데이터를
보유할 수 있을 뿐 아니라 for 루프를 통해 값을 반복적으로 가져올 수 있다.

이러한 내장 반복형 객체만 for 루프에서 사용 가능한 것은 아니다. 반복을 위해 정의한 로직을 사용해
자체 이터러블을 만들 수 있다. 엄밀히 말하면 이터러블은 `__iter__`매직 메서드를 구현한 객체, 이터레이터는
`__next__` 매직 메서드를 구현한 객체를 말한다.

이런 객체를 만들기 위해 매직메서드를 사용할 것이다.

파이썬의 반복은 이터러블 프로토콜이라는 자체 프로토콜을 사용해 동작한다. for e in myobject: 형태로
객체를 반복할 수 있는지 확인하기 위해 파이썬은 고수준에서 다음 두가지를 차례로 검사한다.

- 객체가 `__next__`나 `__iter__` 이터레이터 메서드 중 하나를 포함하는가
- 객체가 시퀀스이고 `__len__`과 `__getitem__`을 모두 가졌는지 여부.

### 이터러블 객체 만들기

객체를 반복하려고 하면 파이썬은 해당 객체의 `iter()` 함수를 호출한다.
이 함수가 처음으로 하는 것은 `__iter__`메서드가 있는지를 확인하는 것이다.

다음은 일정 기간의 날짜를 하루간격으로 반복하는 객체의 코드이다.

```python3
from datetime import timedelta, date

class DateRangeIterable:
    """
    자체 이터레이터 메서드를 가지고 있는 이터러블 객체
    """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today


if __name__ == '__main__':
    r = DateRangeIterable(date(2021, 3, 25), date(2021, 4, 1))

    for day in r:
        print(day)

    for day in r: # 두번째 루프는 동작하지 않는 상태!
        print(day)



"""
output:
2021-03-25
2021-03-26
2021-03-27
2021-03-28
2021-03-29
2021-03-30
2021-03-31
"""


```

for 루프는 앞서 만든 객체를 사용해 새로운 반복을 시작한다. 이제 파이썬은 `iter()` 함수를 호출할 것이고, 이 함수는
`__iter__` 매직 메서드를 호출할 것이다. `__iter__` 메서드는 self를 반환하고 있으므로, 객체 자신이 이터러블임을 나타내고 있다.

따라서 루프의 각 단계마다 자신의 `next()`함수를 호출하고, 이 함수는 다시 `__next__` 메서드에게 위임한다.

이 메서드는 요소를 어떻게 생산하고 하나씩 반환할 것인지 결정한다. 더이상 반환할 것이 없을 경우

`StopIteration` 예외를 발생시켜주어야 한다. for 루프는 결국 StopIteration 예외가 발생할 때 까지 `next()`를 호출하는 것과 같다 !

이 예제에서의 문제는 첫번째 루프에서는 동작을 잘 하지만, 두번째 루프에서는 동작하지 않는다는 점이다.

위 예제에서는 `__iter__` 매직 메서드가 자기 자신을 반환했기 때문이다. 따라서 `__iter__`가 호출될 때 마다 새로운 인스턴스를 만드는것도

그렇게 끔찍한 해결법은 아니지만. `__iter__`에서 제너레이터(이터레이터 객체)를 사용하는 방법이 제일 깔끔하다.

```python3
from datetime import timedelta, date


class DateRangeContainerIterable:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __iter__(self):
        current_day = self.start_date
        while current_day < self.end_date:
            yield current_day
            current_day += timedelta(days=1)


if __name__ == '__main__':
    r = DateRangeContainerIterable(date(2021, 3, 25), date(2021, 4, 1))

    for day in r:
        print(day)

    for day in r:  # 두번째 루프또한 잘 동작한다.
        print(day)


"""
ouput:
2021-03-25
2021-03-26
2021-03-27
2021-03-28
2021-03-29
2021-03-30
2021-03-31
2021-03-25
2021-03-26
2021-03-27
2021-03-28
2021-03-29
2021-03-30
2021-03-31
"""
```

### 제너레이터에 대해서 잠깐 알아보고 가자.

제너레이터는 이터레이터를 생성해주는 함수이다. 이터레이터는 클래스에 위에서 본 각종 매직 메서드를 구현해야 하지만
제너레이터는 함수 안에서 `yield`라는 키워드만 사용하면 끝이다. 그래서 이터레이터보다 훨씬 간단하고 쉽다.

```python3
def gen():
    yield 0
    print('0을 발생시킴')
    yield 1
    print('1을 발생시킴')
    yield 2
    print('2을 발생시킴')


if __name__ == '__main__':
    for i in gen():
        print(i)

"""
output:
0
0을 발생시킴
1
1을 발생시킴
2
2을 발생시킴
"""
```

위 예제를 보고 알 수 있는 점은 yield가 호출될 때 yield 키워드 뒤에있는 값을 함수 외부로 전달한다.
전달한 이후 다시 함수 자신의 로직으로 돌아온다.

따라서 0 이라는 결과가 `print(i)`에 의해 출력 된 이후에, `print('0을 발생시킴')`과 같은 나머지 함수 로직을 탄다는 점이다.

그리고 더이상 yield로 값을 반환하지 못할 경우 `StopIteration` 예외를 발생시킨다.

따라서 이터러블하게 사용이 가능한 것이다.

## 시퀀스 만들기

객체에 `__iter__` 메서드를 정의하지 않았지만, 반복하기를 원하는 경우도  있다.
`iter()`함수는 객체에 `__iter__` 메서드가 정의되어있지 않으면 `__getitem__` 메서드를 찾고 
없으면 `TypeError`를 발생시킨다.

시퀀스는 `__len__`과  `__getitem__`을 구현하고, 첫 번째 인덱스 0부터 시작하여 포함된  요소를
한번에 하나씩 차례로 가져올 수  있어야 한다. 즉 `__getitem__`을 올바르게 구현하여 이러한 인덱싱이
가능하도록 주의를 기울여야 한다.

우리가 바로 직전에서 사용했던 예제는 메모리를 적게 사용한다는 장점이 있다. (제네레이터로 필요할때 만들어 냈으니까.)
즉 한 번에 하나의 날짜만 보관하고 한 번에 하나의 날짜를 생성하는 법을 알고 있었다.

하지만 n번째 요소를 접근하고 싶을 때, 도달할 때 까지 n번 반복한다는 단점이 있다. (그니까 한마디로 연결리스트와 배열의 차이랄까)

이는 CS에서의 전형적인 메모리와 CPU사이의 트레이드 오프다.

이터러블을 사용하면 메모리는 적게 사용하지만, n번째 요소를 얻기 위한 시간복잡도는 O(n)이다.

하지만 시퀀스로 구현한다면 더 많은 메모리가 사용되지만, 특정 요소를 얻기 위한 인덱싱의 시간 복접도는 O(1)이다.

```python3
from datetime import timedelta, date
from typing import List

class DateRangeSequence:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._range = self._create_range()

    def _create_range(self) -> List[date]:
        days = []
        current_day = self.start_date
        while current_day < self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days

    def __getitem__(self, day_no):
        return self._range[day_no]

    def  __len__(self):
        return len(self._range)


if __name__ == '__main__':
    s1 = DateRangeSequence(date(2021, 3, 25), date(2021, 4, 1))

    for day in s1:
        print(day)

    """
    output:
    2021-03-25
    2021-03-26
    2021-03-27
    2021-03-28
    2021-03-29
    2021-03-30
    2021-03-31
    """

    print(s1[0]) # 2021-03-25
    print(s1[3]) # 2021-03-28
    print(s1[-1]) # 2021-03-31

```

## 호출형 객체

함수처럼 동작하는 객체를 정의하면 매우 편리하다!. 가장 흔한 사례는 데코레이터를 만드는 것

매직 메서드 `__call__`을 사용하면 객체를 일반 함수처럼 호출할 수 있다. 여기에 전달된 모든 파라미터는 `__call__`메서드에 그대로 전달된다.

객체를 이렇게 사용하는 주된 이점은 객체에는 상태가 있기 때문에 함수 호출 사이에 정보를 저장할 수 있다는 점이다.

파이썬은 `object(*args, **kwargs)`와 같은 구문을 `object.__call__(*args, **kwargs)`로 변환한다.

이 메서드는 객체를 파라미터가 있는 함수처럼 사용하거나 정보를 기억하는 함수처럼 사용할때 매우 유용하다.

다음은 입력된 파라미터와 동일한 값으로 몇번이나 호출되었는지를 반환하는 객체를 만들 때 `__call__` 매직메서드를 사용하는 예이다.

```python3
from collections import defaultdict


class CallCount:
    def __init__(self):
        self._counts = defaultdict(int)

    def __call__(self, argument):
        self._counts[argument] += 1

        return self._counts[argument]


if __name__ == '__main__':
    cc = CallCount()
    print(cc(1))
    print(cc(2))
    print(cc(1))
    print(cc(3))
    print(cc('hello'))

```

> defaultdict? : defaultdict은 dict의 서브클래스이다. 작동하는 방식은 거의 동일하지만 defaultdict()은 인자로 주어진 객체의 기본값을
> 딕셔너리값의 초깃값으로 지정할 수 있다.
> 즉 defaultdict은 처음 키를 지정할 때 값을 주지 않으면 해당 키에 대한 디폴트 값을 지정하겠다는 의미임 !

### 언제 활용할까??

키의 개수를 세야하는 상황이나, 리스트나 셋의 항목을 정리해야 할 때 사용하면 좋은듯.

```python3
from collections import defaultdict

string = 'dasfsaddafvdafv'

string_dict = defaultdict(int)

for v in string:
    string_dict[v] += 1

print(string_dict) # defaultdict(<class 'int'>, {'d': 4, 'a': 4, 's': 2, 'f': 3, 'v': 2})
```