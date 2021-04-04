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
