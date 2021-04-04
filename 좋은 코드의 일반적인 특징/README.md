# 좋은 코드의 일반적인 특징

이 챕터에서는 좋은 소프트웨어란 무엇인가에 대해서 알아 볼 것.

주로 높은 추상화 수준의 디자인 원칙에 중점을 두고 알아 볼 것이다.

추상화라는 이야기가 자주 나올탠데, 우리가 디테일한 코드의 하나 하나 동작을 신경쓰며 디자인 하는것은
높은 추상화 레벨에서의 디자인이 아닌, 저수준의 디자인이라고 할 수 있다. (소프트웨어 공학에서 저수준, 고수준은 정말
수준이 높고 낮음이 아니다! 좀 더 기계에 가까운지, 사람에게 가까운지의 차이이다.)

저수준의 디자인 뿐만 아니라 높은 추상화 레벨(고수준)의 디자인 원칙도 매우 중요하다.

클린 코드란 코드를 가능한 견고하고, 결함을 최소화하고, 완전히 자명하도록 하는 것이다.

공부할 내용의 목표는 다음과 같다.
- 견고한 소프트웨어의 개념을 이해
- 작업 중 잘못된 데이터를 다루는 방법
- 새로운 요구사항을 쉽게 받아들이고 확장할 수 있는 유지보수가 쉬운 소프트웨어 설계
- 재사용 가능한 소프트웨어 설계
- 개발팀의 생산성을 높이는 효율적인 코드 작성

## 계약에 의한 디자인

소프트웨어는 사용자가 직접 호출하기도 하지만, 코드의 다른 부분에서 호출하는 경우도 있다. 
애플리케이션의 책임을 나누어 레이어나 컴포넌트로 분리한 경우에 그러하다. 이들 서로 간의 교류에 대해서 고민하자.

컴포넌트는 기능을 숨겨 캡슐화하고 함수를 사용할 고객에게는 애플리케이션 프로그래밍 인터페이스(API)를 노출해야 한다.

컴포넌트의 함수, 클래스, 메서드는 특별한 유의사항ㄴ에 따라 동작해야 하며, 그렇지 않을 경우 코드가 깨진다.

반대로 코드를 호출하는 클라이언트는 특정 응답을 기대하며 이것과 다른 경우 함수 호출에 실패하고 결함이 발생한다.

예를 들어 정수를 파라미터로 사용하는 함수에 문자열을 파라미터로 전달하면 기대한 것과 다르게 동작할것이 분명하다.

이러한 경우 절대로 실행되어서도 안되고, 조용히 오류를 발생해도 안된다.

API를 디자인할 때 예상되는 입력, 출력 및 부작용을 문서화해야 한다. 그러나 문서화가 런타임시의 소프트웨어의 동작까지 강제할수는 없다.

이러한 규칙, 정상적으로 동작하기 위해 기대하는 것과 호출자가 반환 받기를 기대하는 것은 디자인의 하나가 되어야 한다.

여기서 계약(contract)라는 개념이 생긴다.

계약에 의한 디자인이란 이런것이다. 관계자가 기대하는 바를 암묵적으로 코드에 삽입하는 대신에 양측이 동의하는 계약을 먼저 한 다음
계약을 어겼을 경우는 명시적으로 왜 계속할 수 없는지 예외를 발생시키라는 것이다.

여기서 말하는 계약은 소프트웨어 컴포넌트 간의 통신 중에 반드시 지켜져야할 몇 가지 규칙을 강제하는 것이다.

계약은 주로 사전조건과 사후조건을 명시하지만 때로는 불변식과 부작용을 기술한다.

- **사전조건** : 코드가 실행되기 전에 체크해야 하는 것들이다. 함수가 진행되기 전에 처리되어야 하는 모든 조건을 처리한다. 
  일반적으로는 파라미터에 주어진 데이터의 유효성을 검사하지만, 유효성 체크를 통해 부작용이 최소화 된다는 점을 고려할때 
  유효성 체크는 많이 하면 할수록 좋다.
  
- **사후조건** : 사전조건과 반대로 여기서는 함수 반환 값의 유효성 검사가 수행된다. 사후조건 검증은
  호출자가 이 컴포넌트에서 기대한 것을 제대로 받았는지 확인하기 위해 수행된다.
  
- **불변식** : 때로는 함수의 독스트링에 불변식에 대해 문서화 하는것이 좋다, 불변식은 함수가 실행되는 동안
  일정하게 유지되는 것으로 함수의 로직에 문제가 없는지 확인하기 위한 것이다.
  
- **부작용** : side-effect. 선택적으로 코드의 부작용을 독스트링에 언급하기도 한다.

이상적으로는 이 모든 것들을 소프트웨어 컴포넌트 계약서의 일부로 문서화 해야하지만, 처음 2개인 사전조건과 사후조건만
저수준(코드) 레벨에서 강제한다.

이렇게 계약에 의한 디자인을 하면 오류가 발생했을때 찾기가 매우 쉽다. 제일 중요한 것은 잘못된 가정 하에 코드의 핵심 부분이 실행되는 것을 방지하기 위해서다.

## 사전조건

사전조건은 함수나 메서드가 제대로 동작하기 위해 보장해야 하는 모든 것을 의미한다. 예를들어 초기화된 객체, null이 아닌 값등의 조건이다.

파이썬은 동적으로 타입이 결정되므로 전달된 데이터가 적절한 타입인지 확인하는 경우도 있다. 

문제는 이 유효성 검사를 어디서 하느냐인데, 클라이언트가 함수를 호출하기 전에 모든 유효성 검사를 하게 할 것인지
함수가 자체적으로 로직을 실행하기 전에 검사하도록 할 것인지에 대한 문제이다.

전자는 관용적인 접근법이라고 부른다. 함수가 어떤 값이라도 수용하기 떄문이다.

후자는 까다로운 접근 방법에 해당한다.

어떤 방식을 택하든 중복 제거 원칙을 항상 마음속에 간직해라. 사전 조건 검증을 양쪽에서 하지 말고 어느 한쪽에서만 해야 한다.

즉 클라이언트에 검증 로직을 두거나, 함수 자체에 두어야 한다. 어떤 경우에도 중복되서는 안된다. (DRY 원칙과 관련)

## 사후조건

사후조건은 메서드 또는 함수가 반환된 후의 상태를 강제하는 계약의 일부이다.

함수 또는 메서드가 적절한 속성으로 호출되었다면 사후조건은 특정 속성이 보존되도록 보장해야한다!

사후조건을 사용하여 클라이언트가 필요로 하는 모든것을 검사할 수 있다. 메서드가 적절히 실행되었다면 계약이 이루어졌으므로
사후조건 검증에 통과하고 클라이언트는 반환 객체를 아무 문제없이 사용할 수 있어야 한다.

## 파이썬스러운 계약

`Programming by Contract for Python`이라는 PEP-316은 현재 연기된 상태. 하지만 이것이
일반적인 디자인 원칙 하에 파이썬으로 구현할 수 없다는 뜻은 아니다.

이를 적용하는 아주 좋은 방법은 아마 함수 및 클래스에 RuntimeError 혹은 ValueError 예외를 발생시키는 제어 메카니즘을 추가하는 것이다.

올바른 예외 타입이 무엇인지 일반적인 규칙을 만드는 것은 애플리케이션 종속적인 부분이 많아서 어렵다.

문제를 정확히 특정하기 어려우면 사용자 정의 예외를 만드는 것이 가장 좋다!

또한 코드를 가능한 격리된 상태로 유지하는것이 좋다. 즉 사전조건에 대한 검사와 사후조건에 대한 검사 그리고 핵심 기능에 대한 구현을 구분하는 것이다.

더 작은 함수를 생성하여 해결할 수도 있지만 데코래이터를 사용하는것이 흥미로운 대안이 될 수 있다.

## 올바른 수준의 추상화 단계에서의 예외처

예외는 오직 한가지 일을 하는 함수의 한 부분이어야 한다. 함수가 처리하는 예외는 캡슐화된 로직과 같아야 함.

아래 예제는 서로 다른 수준의 추상화를 혼합하는 예제. 애플리케이션에서 디코딩한 데이터를 외부 컴포넌트에 전달하는 객체를 상상해보자.

`deliver_event`메서드를 중점으로 봐보자

```python3
from logging import (
    Logger,
    Formatter,
    StreamHandler,
    DEBUG
)
import time

## 로거 설정
logger = Logger('내 로거')
logger.setLevel(DEBUG)  # 로깅 레벨 설정

console = StreamHandler()  # 현재 콘솔에 대한 스트림 핸들러
console.setLevel(DEBUG)  # 현재 콘솔 로깅을 디버그 레벨로 설정(출력)

formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  # 로깅 메시지 포메터

console.setFormatter(formatter)  # 포메터 설정

logger.addHandler(console)  # 내 로거에 콘솔 핸들러 등록


## 로거 설정 완료

class DataTransport:
    """다른 레벨에사 예외처리 하는 객체의 예"""

    retry_threshold: int = 5
    retry_n_times: int = 3

    def __init__(self, connector):
        self._connector = connector
        self.connection = None

    def deliver_event(self, event):
        try:
            self.connect()
            data = event.decode()
            self.send(data)
        except ConnectionError as e:
            logger.info('연결 실패 : %s', e)
            raise  # 로직 예외발생시켜서 중단
        except ValueError as e:
            logger.error('%r 잘못된 데이터 포함: %s', event, e)
            raise

    def connect(self):
        for _ in range(self.retry_n_times):
            try:
                self.connection = self._connector.connect()
            except ConnectionError as e:
                logger.info(
                    '%s: 새로운 연결 시도 %is',
                    e,
                    self.retry_threshold
                )
                time.sleep(self.retry_threshold)
            else:
                return self.connection
        raise ConnectionError(
            f'{self.retry_n_times} 번째 재시도 연결 실패'
        )

    def send(self, data):
        return self.connection.send(data)


```

ValueError와 ConnectionError는 무슨 관계일까? 사실 아무 관계가 없다. 이렇게 매우 다른 유형의
오류를 살펴봄으로써 책임을 어떻게 분산해야 하는지에 대한 아이디어를 얻을 수 있다.

ConnectionError는 connect 메서드 내에서 처리되어야 한다!

connect 메서드가 연결과 관련된 행위의 책임을 갖고 있으니까!

반대로 ValueError는 event의 decode메서드에 속한 에러이다. 이렇게 구현을 수정하면 deliver_event 메서드에서는 예외처리 할 필요가 없다.

이전에 걱정했던 예외는 내부 메서드에서 처리하거나 의도적으로 예외가 발생하도록 내버려 둘 수 있다.

따라서 `deliver_event` 메서드는 다른 메서드나 함수로 분리해야한다. 연결 관리는 작은 함수로 충분하다.

개선된 코드는 다음과 같다.

```python3
from logging import (
    Logger,
    Formatter,
    StreamHandler,
    DEBUG
)
import time

## 로거 설정
logger = Logger('내 로거')
logger.setLevel(DEBUG)  # 로깅 레벨 설정

console = StreamHandler()  # 현재 콘솔에 대한 스트림 핸들러
console.setLevel(DEBUG)  # 현재 콘솔 로깅을 디버그 레벨로 설정(출력)

formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  # 로깅 메시지 포메터

console.setFormatter(formatter)  # 포메터 설정

logger.addHandler(console)  # 내 로거에 콘솔 핸들러 등록


## 로거 설정 완료

def connect_with_retry(connector, retry_n_times, retry_threshold=5):
    """connector와 연결을 맺는다. <retry_n_times> 시도.

    연결에 성공하면 connection 객체 반환
    재시도까지 모두 실패하면 Connection Error 발생

    :param connector: '.connect()'메서드를 가진 객체 
    :param retry_n_times: 'connector.connect()'를 호출하는 횟수
    :param retry_threshold: 재시도 사이의 간격
    :return: connection 객체
    """

    for _ in range(retry_n_times):
        try:
            return connector.connect()
        except ConnectionError as e:  # 리트라이 하기 위해 예외처리 + 로깅을 하는 부분
            logger.info(
                '%s: 새로운 견결 시도 %is', e, retry_threshold
            )
            time.sleep(retry_threshold)
    # 위에서 Connetion Error를 5번까지 처리하고 로깅하다가.
    # 이 아래 로직으로 넘어왔다는건 결국 연결에 실패했다는 의미. 예외를 발생시켜주면 된다.
    exc = ConnectionError(f'{retry_n_times} 번재 째시도 연결 실패')
    logger.exception(exc)
    raise exc


class DataTransport:
    """다른 레벨에사 예외처리 하는 객체의 예"""

    retry_threshold: int = 5
    retry_n_times: int = 3

    def __init__(self, connector):
        self._connector = connector
        self.connection = None

    def deliver_event(self, event):
        self.connection = connect_with_retry(
            self._connector, self.retry_n_times, self.retry_threshold
        )
        self.send(event)

    def send(self, event):
        try:
            return self.connection.send(event.decode())
        except ValueError as e:
            logger.error('%r 잘못된 데이터 포함: %s', event, e)
            raise

```

각 메서드는 자신이 처리해야하는 예외만 처리한다. connect 메서드는 함수로 따로 분리하여서 예외처리를 한다.

각 메서드는 훨씬 작아졌고, 읽기도 쉬워졌다. 이렇게 메서드를 따로 함수로 분리하는 접근 괜찮아 보인다.
