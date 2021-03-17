# 객체지향 디자인의 기본 원칙

## 개방 - 폐쇄 원칙
개방-폐쇄 원칙이란 클래스와 객체, 메소드 모두 확장엔 개방적이고 수정엔 폐쇄적이어야 한다는 원칙이다.   

클래스 또는 객체의 기능을 확장할 때, 기본 클래스 자체를 수정하지 않아도 되도록 클래스와 모듈을 설계해야 한다.   
클래스 확장만으로 새로운 기능을 구현 할 수 있어야 한다.

(그러니까, 뼈대가되는 베이스 클래스를 수정하지 않고, 구현체인 자식 클래스의 수정으로 기능이 추가되어야 한다는 소리지?)

추상 클래스를 수정하지 않고 확장해서 새로운 기능을 추가하는 것이 개방-폐쇄의 원칙을 따르는 것

- 장점
    - 기존 클래스를 변경하지 않기 때문에 문제가 발생할 가능성이 낮다.
    - 기존 버전과의 호환성 유지가 수월하다.
    
## 제어 반전 원칙(IoC)
제어 반전 원칙이란 상위 모듈은 하위 모듈에 의존적이지 않아야 한다는 원칙이다.  
가능한 모두 추상화에 의존해야 한다. 추상화가 세부 사항에 의존하는 상황은 바람직하지 않다.

이 원칙에 의하면 모듈은 지나치게 상호 의존하지 않아야 한다. 추상화를 통해 기본 모듈과 종속 모듈을 분리해야 한다.  

제어 반전 원칙은 클랴스의 세부 내용은 추상화돼야 한다는 것을 의미하기도 한다,
세부 구현이 추상화를 결정하는 것은 반드시 피해야 한다.

- 제어 반전 원칙의 장점
    - 모듈 간의 낮은 상호 의존도는 시스템 복잡도를 줄인다.
    - 종속 모듈 사이에 명확한 추상화 계층(훅 또는 매개 변수를 통해 지원)이 있기 때문에 모듈간의 종속 관계를 쉽게 알 수 있다.
    
IoC/DI 라고도 부르나 보다. (Inversion of Control / Dependency Injection)

제어의 반전과 의존성 주입

의존성 주입이란 프로그래밍에서 구성요소간의 의존 관계가 소스코드 내부가 아닌 외부로부터 오도록 하는건데...

유형은 다음과 같다.
- 생성자 주입
- setter를 통한 주입
- 인터페이스를 통한 주입

- 장점
    - 결합도 낮음
    - 재사용성
    - 테스트 편의성
    
즉 객체간의 강한 결합을 깨주는 역할을 한다고 보면 되겠다.

before
```python
import os

class ApiClient:

    def __init__(self):
        self.api_key = os.getenv('API_KEY')  # 의존 : 강한 결합
        self.timeout = os.getenv('TIMEOUT')  # 의존
        # 설명하자면.. 이 클래스의 속성을 이렇게 단순히 설정하게 되면
        # 의존성이 강해진다고 이야기 하는 것 같다. 
        # 인스턴스화 할 때 따로 인자로 주어서 속성을 정의 할 수 없으니까 (추후에 속성을 접근해서 뭐 수정은 가능하겠지만)
        # 그렇지 아니하고, 인스턴스화 할 때 생성자를 통해 옵션으로 받을 수 있게 리팩토링 해야겠지?

class Service:

    def __init__(self):
        self.api_client = ApiClient()  # 의존성


def main() -> None:
    service = Service()  # 의존성이 생겼다 !
    ...


if __name__ == '__main__':
    main()
```

after

```python
import os

class ApiClient:

    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key  # 생성자를 통한 의존성 주입
        self.timeout = timeout  # 이렇게 하면, 이제 실제로 이 클래스를 인스턴스화 할 때 당시에 설정을 해줄 수 있으니까. 


class Service:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client  # 역시나 의존성 주입


def main(service: Service):  
    pass


if __name__ == '__main__':
    main(
        service=Service(
            api_client=ApiClient(
                api_key=os.getenv('API_KEY'),
                timeout=os.getenv('TIMEOUT'),
            ),
        ),
    )
```

- 정리하자면.. 의존성 주입 및 제어의 역전을 사용해야
- 사용자가 쉽게 사용도 가능한 장점도 있고
- 대부분의 프레임워크는 제어의 반전 및 의존성 주입을 매우 활발하게 사용함

아래 코드는 `Django`에서 발췌

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL + '/1',
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'snowflake',
    }
}
```

```python
class FooView(APIView):
    # 주입된 의존성들
    permission_classes = (IsAuthenticated, )
    throttle_classes = (ScopedRateThrottle, )
    parser_classes = (parsers.FormParser, parsers.JSONParser, parsers.MultiPartParser)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
```

> "Dependency Injection" is a 25-dollar term for a 5-cent
> concept. [...] Dependency injection means giving an object
> its instance variables. [...].


> 의존성 주입은 5센트짜리 컨셉으로 25달러(무려 500배)의 효과를 발휘 할 수 있는 컨셉이다.
> 의존성 주입은 인스턴스의 생성당시 인자로 객체를 제공하는것을 의미한다.

- 간단히 정리하자면, 의존성 주입이라는거는 인스턴스화 할때 클래스의 생성자나 기타 메서드에 `object`를 인자로 주는것을 의미한다.
- 최근 사이드 프로젝트에서 `Sequelize`를 사용하면서 인스턴스화 할 때 객체를 인자로 주었었는데, 이게 바로 생성자를 통한 의존성 주입에 해당되는거겠지...

파이썬은 아니지만 `Sequelize` 의존성 주입 예시

```js
const Sequelize = require('sequelize');
const env = process.env.NODE_ENV || 'development';
const {development, production, test} = require('../config/config');
const db = {};

const sequelize = new Sequelize(
  development.database,
  development.username,
  development.password,
  development
); //객체들로 인자를 주는 형태?
```

자바에서의 의존성 주입 및 제어의 반전 예시

before
```java
public class TextEditor {

    private SpellChecker checker;

    public TextEditor() {
        this.checker = new SpellChecker();
    }
}
```

after
```java
public class TextEditor {

    private IocSpellChecker checker;

    public TextEditor(IocSpellChecker checker) {
        this.checker = checker;
    }
}
```

## 인터페이스 분리 원칙

인터페이스 분리의 원칙(The interface Segregation Principle)이란 클라이언트는 불필요한 인터페이스에 의존하지 않아야 한다는 원칙이다.

이 원칙은 효율적인 인터페이스 작성을 유도한다. 개발자는 반드시 해당 기능과 관련 있는 메서드만을 작성해야 한다. 해당 인터페이스와
상관없는 메서드를 포함하는 인터페이스를 구현하는 모든 구현체 클래스는 필요없는 메서드까지 구현해야 하니까..

예를들어 `Pizza`인터페이스에는 `add_chicken()`과 같은 메서드가 필요하지 않다.
`Pizza` 인터페이스를 구현하는 `Veg Pizza` 클래스에 이런 메서드를 강요하면 안되지 않겠어?

인터페이스 분리 원칙의 장점은 다음과 같다.
- 인터페이스에 꼭 필요한 메서드만 포함하는 가벼운 인터페이스를 작성할 수 있다.
- 인터페이스에 불필요한 메서드가 포함되는 것을 방지한다.

**인터페이스 분리의 원칙을 위배한 코드**

```python3
import abc


class Shape(metaclass=abc.ABCMeta):
    """A demo shape class"""

    @abc.abstractmethod
    def draw_circle(self):
        """Draw a circle"""
        raise NotImplemented

    @abc.abstractmethod
    def draw_square(self):
        """ Draw a square"""
        raise NotImplemented


class Circle(Shape):
    """A demo circle class"""

    def draw_circle(self):
        """
        원을 그리는 메서드
        :param  None
        :return: None
        """
        print("원 그리기 !")

    def draw_square(self):
        """
        사각형을 그리는 메서드 사용하지 않음.
        """
        pass


if __name__ == '__main__':
    circle = Circle()
    circle.draw_circle()

```

위 코드의 문제점 :
- `shape`라는 인터페이스에, `draw_circle`, `draw_square`등 추상적이지 아니한 너무 많은 메서드를 추가함
- 따라서 구현체 클래스에서 저 놈들을 쓸데없이 다 구현해야 함

**리팩토링된 코드**

```python3
import abc


class Shape(metaclass=abc.ABCMeta):
    """A demo shape class"""
    
    @abc.abstractmethod
    def draw(self):
        """Draw a shape"""
        raise NotImplemented


class Circle(Shape):
    """A demo circle class"""

    def draw(self):
        """Draw a circle"""
        pass


class Square(Shape):
    """A demo square class"""

    def draw(self):
        """Draw a square"""
        pass

```

이렇게 각 구현체 클래스에서 자신의 특성에 맞는 로직을 따로 짜도록 인터페이스 클래스는 최대한 추상화해서 필요한 메서드만 작성해주어야 한다!


## 단일책임의 원칙

단일 책임 원칙(The Single Responsibility Principle)이란 클래스는 하나의 책임만을 가져야 한다는 원칙이다.

클래스를 구현할 때 한 가지 기능에만 중점을 두어야 한다. 두 가지 이상의 기능이 필요하다면 클래스를 나눠야 한다.
이 원칙에서는 클래스는 기능으로 인해 변경된다. 특정 기능의 작동 방식이 변경돼 클래스를 수정하는 것은 허용되지만 두 가지 이상의 이유(두가지 기능 변경)
때문에 클래스를 수정해야 한다면 클래스는 분할돼야 한다.

단일 책임 원칙의 장점은 다음과 같다.

- 어떤 기능을 수정할 때 특정 클래스만 변경된다.
- 한 개의 클래스에 여러 기능이 있는 경우, 종속된 클래스도 기본 클래스의 역할을 완전히 치환하 수 있어야 한다는 원칙이다.

생각해보면 디자인 패턴에서 제시하는 여러 패턴들은 단일책임 원칙을 매우 잘 지키고 있다고 생각하면 되는데,

대표적으로 생성자 패턴에서의 팩토리패턴을 생각해보자.

팩토리 패턴이라는건, 객체를 찍어낼(인스턴를 만들어낼)팩토리 클래스와 실제로 객체를 찍어낼 틀(클래스)가 각자의 기능이 분리되어있는 형태다.

그래서 유지보수도 쉬워지기도 하는거지..

단일 책임 기능의 원칙을 위반하고, 하나의 클래스에 너무 많은 기능을 떄려박으면, `God Class`라고 부르는 정말 모든걸 다하는 신의 클래스를 만들게 된다!

### 주의점 !

몇몇 사람들은 이 단일책임의 원칙이 오직 객체지향 프로그래밍 패러다임에서만 적용된다고 오해 하기도 하는데,
이 단일책임 원칙은 모든 소프트웨어 개발 패러다임에서 적용된다.

그러니까 함수형 프로그래밍을 하고 있을 지라도 단일 책임 원칙은 꼭 잘 지키라는 의미다!

나 같은 초짜 개발자들이 대표적으로 하는 실수가 이 단일책임 원칙을 위배하는것!

아래와 같은 코드를 생각해보자

```python3
 def percentage_of_word(search, file):
    search = search.lower()
    content = open(file, "r").read()
    words = content.split()
    number_of_words = len(words)
    occurrences = 0
    for word in words:
        if word.lower() == search:
            occurrences += 1
    return occurrences/number_of_words
```

위 코드는 인자로 주어진 search 스트링(단어)이 file 이라는 인자로 주어진 파일이 갖고있는 단어중에서
얼마나 많이 겹치는지 퍼센티지를 계산하는 함수이다.

겉으로 보기엔 하나의 기능만 한다고 생각 할 수도 있지만

1. 파일을 열고
2. 단어의 개수를 새고
3. 얼마나 자주 나왔는지 카운트하고
4. 퍼센티지를 계산하는

이렇게 여러 기능을 벌써 하고 있는것이다.

위 코드는 아래와 같이 리팩토링이 가능하다.

```python3
def read_localfile(file):
    """파일을 읽는 함수"""

    return open(file, "r").read()


def number_of_words(content):
    """파일에 있는 단어의 개수"""

    return len(content.split())


def count_word_occurrences(word, content):
    """해당 파일에 얼마나 자주 word가 등장하는지 카운트하는 함수"""

    counter = 0
    for e in content.split():
        if word.lower() == e.lower():
            counter += 1
    return counter


def percentage_of_word(word, content):
    """전체 단어들 중 word에 해당하는 단어가 얼마의 비율로 나타나는지 계산하는 함수(퍼센티지 계산)"""

    total_words = number_of_words(content)
    word_occurrences = count_word_occurrences(word, content)
    return word_occurrences/total_words


def percentage_of_word_in_localfile(word, file):
    """텍스트 파일에 있는 단어들 중 word에 해당하는 단어가 얼마의 비율로 나타는지 계산하는 함수"""

    content = read_localfile(file)
    return percentage_of_word(word, content)
```

분리된 각 함수는 오직 하나의 기능만을 충실하게 수행하도록 변경되었다 !

## 치환 원칙

치환 원칙(The Substitution Principle)이란 상속받는 클래스는 기본 클래스의 역할을 완전히 치환 할 수 있어야 한다는 원칙이다.
말 그대로 파생된 클래스는 기본 클래스를 완전히 확장해야 한다는 의미다.

코드 수정 또는 추가 없이도 파생된 클래스는 기본 클래스를 대체 할 수 있어야 한다.

### 치환 원을 위배한 코드

```python3
class Calculator():
    def calculate(self, a, b): # returns a number
        return a * b

class DividerCalculator(Calculator):
    def calculate(self, a, b): # returns a number or raises an Error
        return a / b           

calculation_results = [
    Calculator().calculate(3, 4),
    Calculator().calculate(5, 7),
    DividerCalculator().calculate(3, 4),
    DividerCalculator().calculate(5, 0) # 0 will cause an Error
]

print(calculation_results)
```

출력

```console
ZeroDivisionError: division by zero
```
위 코드는 치환 원칙을 위배한 코드이다. 

모든 `Calculator`의 서브 클래스들은 `calculation`이라는 숫자를 리턴하는 메서드를 구현해야 한다.

위 코드는

1. 클래스의 계층 구조를 수정하거나
2. 모든 `calculation` 메서드를 `try/except` 구문 안에서 호출

위 두가지를 하지 않는 이상 버그를 고칠 수 없다.

`DividerCalculator` 클래스는 `Calculator` 클래스와 이러한 부분에서 다르다.

- **두 값을 곱한것** 은 항상 숫자형을 리턴한다.
- **두 값을 나눈것** 은 에러를 발생 시킬 수 있음 (ZeroDivisionError)

위 결과는 리턴형의 타입이 다르기 때문에, 인터페이스도 다르다고 할 수 있다.
곱하기와 나누기는 절대로 같은것이 아니다(아까 위에서 예기한 예외가 발생하기도 하고, 정수만을 인자로 받는다고 할 때 곱하기는 정수형을 리턴하지만, 나누기는 실수형을 리턴한다 !) . 그러니까 이렇게 클래스 및 메서드를 상속받아 구현하는게 아니라...
다른 것을 통해서 파생되어야 한다는 이야기다!

### 또 다른 치환 원칙을 위배한 그지같은 코드들을 소개한다.

```python3
class Line(Shape):
    def calculate_surface_area(self):
        return -1 # Line이라는건 면적을 가질 수 없다 !
    

class Manager(Employee):
    def desk_id(self):
        return "" # 매니저는 보통 desk에서 일하지 않고 보통 미팅룸에서 일한다
    

class CompletedTask(Task):
    def complete(self):
        raise Exception("Cannot complete a completed task")
        # ??????????????????
```

치환 원칙을 위배하는 코드는 보통 다음과 같은 상황에서 나옵니다.
T 클래스로부터 S 클래스를 상속받습니다. S와 T클래스는 서로 관련이 있어 보이지만, 
하나, 혹은 그 이상의 기능적인 인터페이스(메서드)가 다를 때 발생합니다.

이러한 문제를 해결하기 위해서는 클래스 계층에서의 추상화 정도를 증가시키거나, 감소시키는 방법으로 해결합니다.

![image1](https://i.stack.imgur.com/ilxzO.jpg)

- 치환 원칙을 위배하면 발생하는 이슈를 보여주는 그림

## 디자인 패턴의 개념

디자인 패턴은 GoF(Gang of Four)가 주어진 여러 문제에 대한 해결책으로 제시했다.
GoF란 GoF의 디자인 패턴을 집필한 네명의 저자를 지칭한다.

이 책은 소프웨어 설계 단계에서 흔히 발생하는 여러 문제의 해결책으로 총 23개의 디자인 패턴을 제시하며,
자바를 기반으로 한다. 디자인 패턴이라는 개념은 발명보다 발견에 가깝다.

디자인 패턴의 주요 기능은 다음과 같다.

1. 언어에 독립적이며 모든 프로그래밍 언어에 적용 할 수 있다.
2. 새로운 패턴이 아직도 연구되고 있다.
3. 목적에 맞게 변경될 수 있기 때문에 개발자에게 유용하다.

디자인 패턴에 대한 개발자의 인식은 대개 다음과 같다.

1. 디자인 패턴은 모든 디자인 문제의 만병통치약이다.
2. 문제를 해결하는 훌륭한 해결책이다.
3. 대부분의 개발자가 인정하는 해결책이다.
4. 패턴이라는 단어는 디자인에 반복적인 요소가 있다는 것을 나타낸다.

문제를 자체적으로 해결해보려고 노력해도 결과가 불완전한 경우가 많다. 디자인 패턴은 완성도를 보장한다.
완성도란 디자인과 확장성, 재활용성, 효율성 등을 모두 포함한다.

디자인 패턴은 실패를 통해 배우기보단, 이미 입중된 해결책을 통해 배워야 한다.

디자인 패턴을 언제 사용해야 하는지도 흥미로운 논제거리다. 소프트웨어 개발 사이클의 분석과 설계 단계 중
언제 사용하는 것이 맞는지에 대한 논쟁이 있다.

## 디자인 패턴의 장점
1. 여러 프로젝트에서 재사용 될 수 있다.
2. 설계 문제를 해결 할 수 있다.
3. 오랜 시간에 걸쳐 유효성이 입증되었다.
4. 신뢰 할 수 있는 솔루션이다.

## 디자인 패턴 용어

1. 스니펫 : 데이터베이스에 연결하는 파이썬 코드 등, 특수한 목적을 위한 코드
2. 디자인 : 특정 문제를 해결하기 위한 해결책
3. 스탠다드 : 문제를 해결하는 대표적인 방식, 포괄적이며 현재 상황에 적합한 방식
4. 패턴 : 유사한 문제들을 모두 해결 할 수 있는 유효성이 검증 된 효율적인 해결책

## 디자인 패턴의 분류

- 생성 패턴
- 구조 패턴
- 행위 패턴

## 생성 패턴
- 객체가 생성되는 방식을 기반으로 작동한다.
- 객체 생성 관련 상세 로직을 숨긴다.
- 코드와 생성되는 객체의 클래스는 서로 독립적이다.

## 구조 패턴
- 클래스와 객체를 더 큰 결과물로 합칠 수 있는 구조로 설계한다.
- 구조가 단순해지고, 클래스와 객체 간의 상호관계를 파악 할 수 있다.
- 클래스 상속과 컴포지션에 의존한다.

## 행위 패턴
- 객체 간의 상호작용과 책임을 기반으로 작동한다.
- 객체는 상호작용하지만 느슨하게 결합되어야 한다.

