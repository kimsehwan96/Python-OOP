def stop_database():
    print('stop')


def start_database():
    print('start')


class DBHandler(object):
    """
    DB가 오프라인 상태에서만 작업하기 위한 DB 핸들러
    """

    def __enter__(self):
        stop_database()
        return self  # 굳이 반환값이 없어도 되지만, 웬만하면 객체 자신을 리턴해주는 것으로 구현하자 !

    def __exit__(self, exc_type, exc_val, exc_tb):
        start_database()  # 컨텍스트 관리자를 탈출한 이후에 DB를 스타트


def db_backup():
    print("db backup start")


if __name__ == "__main__":
    with DBHandler():
        db_backup()
