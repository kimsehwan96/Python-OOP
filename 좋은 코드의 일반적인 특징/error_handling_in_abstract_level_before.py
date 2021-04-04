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
