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