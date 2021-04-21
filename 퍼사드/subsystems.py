class Hotelier:
    def __init__(self):
        print('Hotelier instantiate')

    def _is_availale(self) -> bool:
        print("호텔이 예약 가능한지 알아보겠습니다.")
        # 예제니까 무조건 참을 반환하자
        return True

    def book_hotel(self):
        if self._is_availale():
            print("호텔을 예약했습니다.\n\n")


class Florist:
    def __init__(self):
        print('Florist instantiate')

    def set_flower_requirements(self):
        print('꽃 장식을 다 완료했습니다. \n\n')


class Caterer:
    def __init__(self):
        print('Caterer instantiate')

    def set_cuisine(self):
        print('음식 준비를 완료했습니다. \n\n')


class Musician:
    def __init__(self):
        print('Musician instantiate')

    def set_music_type(self):
        print('재즈와 클래식 연주를 준비하겠습니다.')

