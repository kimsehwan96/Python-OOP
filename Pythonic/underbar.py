class Connector:
    def __init__(self, source):
        self.source = source
        self._timeout = 60

conn = Connector('postgresql://localhost:1234')
conn.source # 'postgresql://localhost:1234'
conn._timeout # 60

conn.__dict__  # {'source': 'postgresql://localhost:1234', '_timeout': 60}