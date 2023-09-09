from dataclasses import dataclass
from datetime import date, time


@dataclass
class Time:
    hour: int
    minute: int
    second: int

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)
        if args:
            self.hour, self.minute, self.second = map(int, args[0].split(':'))
        self.__valid()

    def __valid(self):
        if not 0 <= self.hour <= 23:
            raise ValueError('hour must be in 0..23', self.hour)
        if not 0 <= self.minute <= 59:
            raise ValueError('minute must be in 0..59', self.minute)
        if not 0 <= self.second <= 59:
            raise ValueError('second must be in 0..59', self.second)


@dataclass
class ScraperModel:
    id: int
    token: str
    start_time: Time
    end_time: Time
    name: str
    can_work: bool

    def __init__(self, json: dict):
        fields = self.__class__.__dict__.get('__annotations__')
        for k, v in fields.items():
            self.__dict__[k] = v(json.get(k))

