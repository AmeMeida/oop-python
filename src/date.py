class Data:
    # quantidade de dias desde 1 de janeiro de 1970
    _days: int

    def __init__(self, date: str) -> None:
        self._days = to_days(date)

    @property
    def days(self):
        return self._days

    def __str__(self) -> str:
        return str(self._days)

    def __sub__(self, other_date):
        return self.days - other_date.days

def is_leap(year: int) -> bool:
    return (year & 0b11 == 0) and (not (year % 100 == 0) or (year % 400 == 0))

def to_days(date: str):
    day, month, year = map(int, date.split('/'))

    day_gap = 0

    for year in range(1970, year):
        if is_leap(year):
            day_gap += 1

        day_gap += 365

    for month in range(1, month):
        if month == 2:
            day_gap += 28 + is_leap(year)
            continue

        if month >= 8:
            month -= 1

        day_gap += 30 + (month & 0b1)

    day_gap += day

    return day_gap

if __name__ == "__main__":
    print(to_days("18/03/2024"))
    print(to_days("18/03/2010"))
    print(to_days("18/03/2023"))
