# 옵저버 패턴

`퍼사드`, `프록시`가 구조 패턴이고, `팩토리`, `싱글톤`이 생성 패턴이였다면 옵저버 패턴은 `행위 패턴`중 하나이다. 

## 행위 패턴 개요

생성 패턴에서는 객체가 생성되는 방식이 중요했다. 객체가 생성되는 세부 과정은 숨기고, 생성하려는 객체 형과 독립적인 구조를 지원한다.

구조 패턴은 객체와 클래스를 합쳐서 더 큰 기능을 구현한다. 구조를 간소화 하고 클래스와 객체 사이의 관계를 찾는것이 주목적이다.

행위 패턴은 객체의 역할(행동)에 초점을 둔다. 더 큰 기능을 구현하기 위해 객체 간의 상호 작용을 중요시 한다. 행동 패턴에서는 객체는 상호작용 하지만 느슨하게 결합돼있다.
옵저버 패턴은 가장 단순한 행위 패턴이다.

## 옵저버 패턴 이해

옵저버 패턴에서 객체는 자식의 목록을 유지하며 객체가 자식에 정의된 메소드를 호출할 때 마다 옵저버에 이를 알린다.

간단하게 생각해서 브로드캐스트나, pub/sub 구조를 같은 시스템에서 옵저버 디자인 패턴이 자주 사용된다.

옵저버 패턴의 목적은 다음과 같다.

- 객체간 일대다 관계를 형성하고 객체의 상태를 다른 종속 객체에 자동으로 알린다.
- 서브젝트의 핵심 부분을 캡슐화 한다.

옵저버 패턴은 다음과 같은 상황에 매우 적합하다!

- 분산 시스템의 이벤트 서비스를 구현 할 때
- 뉴스 에이전시 프레임워크 (새글이 올라오면 뭐 확인하는 그런건가..?)
- 주식 시장 모델


## 파이썬 코드 예시

```python3
class Subject:
    def __init__(self):
        self.__observers = []

    def register(self, observer):
        self.__observers.append(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer:
    def __init__(self, subject, name: str):
        self._name = name
        subject.register(self)

    def notify(self, subject, *args, **kwargs):
        print(f'{self._name} got args: {args}, kwargs: {kwargs} from {subject}')


if __name__ == '__main__':
    subject = Subject()
    ob1 = Observer(subject, 'ob1')
    ob2 = Observer(subject, 'ob2')

    subject.notify_all('notification!', keyword='value')
    
    
"""
result:
ob1 got args: ('notification!',), kwargs: {'keyword': 'value'} from <__main__.Subject object at 0x7fa3c88c1950>
ob2 got args: ('notification!',), kwargs: {'keyword': 'value'} from <__main__.Subject object at 0x7fa3c88c1950>
"""
```

