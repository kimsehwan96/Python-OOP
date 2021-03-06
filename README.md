# 파이썬 OOP

- 기초적인 내용부터 심화 내용까지 차근 차근 정리하기

##  객체지향

### 객체
- 프로그램 내 개체를 나타낸다.
- 개체는 다른 개체와 상호작용하며 목적을 달성한다

### 클래스
- 클래스는 속성과 행동을 포함하는 객체를 정의한다.
- 속성은 데이터의 요소이고 함수는 특정 작업을 수행한다.
- 클래스에는 객체의 초기 상태를 설정하는 생성자가 있다.
- 클래스는 일종의 템플릿으로 쉽게 재사용 될 수 있다.

### 메소드
- 객체의 행위를 나타낸다
- 속성을 조작하고 작업을 수행한다.

### 캡슐화

- 객체의 기능과 상태를 외부로부터 은닉한다.
- 클라이언트는 객체의 내부구조 및 상태를 직접 수정 할 수 없고 수정을 요청한다.
- 요청의 종류에 따라 객체는 get, set과 같은 특수 함수를 사용해 내부 상태를 변경한다.
- 파이썬은 public, private, protected와 같은 접근 제어 키워드가 없다.
- 하지만 `_` 과 `__`을 활용해 비슷하게 사용 가능하다.

### 다형성

- 다형성의 두가지 의미
    - 객체는 전달 인자에 따라 다른 메소드를 호출한다.
    - 동일한 인터페이스를 여러 형식의 객체들이 공유한다.
    
- 파이썬은 다형성을 지원하는 언어다. + 연산자는 숫자를 더할때, 문자열을 합칠때 모두 사용 가능하다.

### 상속
- 상속은 클래스의 기능이 부모 클래스로부터 파생되는 것을 의미
- 부모 클래스에 정의된 함수를 재사용 할 수 있고, 소프트웨어의 기본 구현을 확장시킬 수 있다.
- 상속은 여러 클래스의 객체의 상호작용을 기반으로 계층을 형성한다. 파이썬은 다중상속 허용

### 추상화
- 클라이언트가 클래스 객체를 생성하고 인터페이스에 정의된 함수를 호출 할  수  있다.
- 클라이언트는 클래스의 복잡한 내부 구현에 대한 이해 없이 간편하게 인터페이스 사용 가능

```python3
class Adder:
    def __init__(self):
        self.num = 0
    def add(self, value):
        self.num += value 

acc = Adder()

for i in range(99):
    acc.add(i)
```

### 컴포지션

- 객체나 클래스를 더 복잡한 자료 구조나 모듈로 묶는 행위이다.
- 컴포지션을 통해 특정 객체는 다른 모듈의 함수를 호출 할 수 있다. 즉 상속 없이 외부기능을 사용 할 수 있다.

```python3
class A(object):
    def a1(self):
        print("a1")

class B(object):
    def b(self):
        print('b')
        A().a1() #상속 없이 외부 클래스의 메서드를 호출했다. 이것이 컴포지션
        
objectB = B()
objectB.b() # b a1
    
```

### 상속과 컴포지션의 차이점?

- 상속은 일반적으로 암시적 선언이라고 부르며
- 컴포지션은 일반적으로 명시적 선언이라고 부른다.

상속은 자식 클래스가 부모 클래스의 모든 속성을 물려받는 반면  
컴포지션은 자식클래스가 필요한 속성만 부모클래스로부터 받아와 사용한다.

상속과 컴포지션은 단순히 별개의 것이 아니고, 기존의 클래스를 재사용하는 상황에 있어서  
상속을 사용해야 할지, 컴포지션을 사용해야 할 지 신중히 판단해야 한다.

s