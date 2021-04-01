from datetime import timedelta, date

class DateRangeIterable:
    """
    자체 이터레이터 메서드를 가지고 있는 이터러블 객체
    """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today


if __name__ == '__main__':
    r = DateRangeIterable(date(2021, 3, 25), date(2021, 4, 1))

    for day in r:
        print(day)

    for day in r: # 두번째 루프는 동작하지 않는 상태!
        print(day)



"""
output:
2021-03-25
2021-03-26
2021-03-27
2021-03-28
2021-03-29
2021-03-30
2021-03-31
"""

