from collections import defaultdict

int_dict = defaultdict(int)
print(int_dict)  # defaultdict(<class 'int'>, {}) <- 디폴트값이 int인 딕셔너리다!

print(int_dict['key1'])  # 0
print(int_dict)  # defaultdict(<class 'int'>, {'key1': 0})

# 키를 단순히 설정하면 값을 지정하지 않은 키는 그 값이 0으로 지정됨!
# 키에 값을 명시적으로 지정하면 그 값이 저장되구!

int_dict['key2'] = 'hello'

print(int_dict)  # defaultdict(<class 'int'>, {'key1': 0, 'key2': 'hello'})

# 이번엔 디폴트가 str인 딕셔너리 만들어볼까?

str_dict = defaultdict(str)

print(str_dict)  # defaultdict(<class 'str'>, {})

str_dict['key1']

print(str_dict)  # defaultdict(<class 'str'>, {'key1': ''})


# 디폴트값이 '' 이 나왔다!

# 커스텀 클래스로 default dict 만들기 테스트 중..
class CustomType:
    def __init__(self, data='Null'):
        self._type = 'custom'
        self._data = data

    def __str__(self):
        return self._data

    def __repr__(self):
        return self.__str__()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: str):
        self._data = data


c_dict = defaultdict(CustomType)
print(c_dict) # defaultdict(<class '__main__.CustomType'>, {})
c_dict['key1'] # defaultdict(<class '__main__.CustomType'>, {'key1': Null})
print(c_dict) # <class '__main__.CustomType'>

print(type(c_dict.get('key1')))
