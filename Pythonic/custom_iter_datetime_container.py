from datetime import timedelta, date


class DateRangeContainerIterable:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __iter__(self):
        current_day = self.start_date
        while current_day < self.end_date:
            yield current_day
            current_day += timedelta(days=1)


if __name__ == '__main__':
    r = DateRangeContainerIterable(date(2021, 3, 25), date(2021, 4, 1))

    for day in r:
        print(day)

    for day in r:  # 두번째 루프또한 잘 동작한다.
        print(day)


"""
ouput:
2021-03-25
2021-03-26
2021-03-27
2021-03-28
2021-03-29
2021-03-30
2021-03-31
2021-03-25
2021-03-26
2021-03-27
2021-03-28
2021-03-29
2021-03-30
2021-03-31
"""