import re
import datetime
from easy_file.cast.patterns.c_patterns import CPattern
from easy_file.cast.utils import get_group


class CDate:
    patterns = None
    type = 'DATE'
    patterns_table = 'date_patterns'

    @staticmethod
    def cast(value):
        for m in [CDate._cast]:
            res = m(value)
            if res:
                return res
        return None

    @staticmethod
    def _cast(value):
        CDate.patterns = CPattern.get_patterns(CDate.patterns_table)
        for p in CDate.patterns:
            m = re.match(p.pattern, value)
            if m is None:
                continue

            res = CDate.get_date(m)
            return {'initial_value': value,
                    'value': res,
                    **p.__dict__}
        return {'initial_value': value,
                'value': None}

    @staticmethod
    def get_date(m):
        year = get_group(m, 'year')
        month = get_group(m, 'month')
        day = get_group(m, 'day')
        week = get_group(m, 'week')
        day_number = get_group(m, 'day_number')

        if year and month and day:
            return datetime.date(year=int(year),
                                 month=int(month),
                                 day=int(day))
        elif year and week and day_number:
            return datetime.date.fromisocalendar(int(year),
                                                 int(week),
                                                 int(day_number))
        return None

    @staticmethod
    def convert_to(value):
        res = CDate.cast(value)['value']
        if res is not None:
            return res
        return None
