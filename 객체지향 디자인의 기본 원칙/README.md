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
