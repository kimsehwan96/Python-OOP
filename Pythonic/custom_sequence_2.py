from datetime import timedelta, date
from typing import List

class DateRangeSequence:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._range = self._create_range()

    def _create_range(self) -> List[date]:
        days = []
        current_day = self.start_date
        while current_day < self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days

    def __getitem__(self, day_no):
        return self._range[day_no]

    def  __len__(self):
        return len(self._range)


if __name__ == '__main__':
    s1 = DateRangeSequence(date(2021, 3, 25), date(2021, 4, 1))

    for day in s1:
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

    print(s1[0]) # 2021-03-25
    print(s1[3]) # 2021-03-28
    print(s1[-1]) # 2021-03-31
