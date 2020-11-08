import re
from easy_file.cast.patterns.c_patterns import CPattern


class CInteger:
    patterns = None
    type = 'INTEGER'
    patterns_file_name = 'integer.json'
    patterns_table = 'integer_patterns'

    @staticmethod
    def _cast(value):
        val = value.replace(' ', '')
        CInteger.patterns = CPattern.get_patterns(CInteger.patterns_table)
        for p in CInteger.patterns:
            m = re.match(p.pattern, val)
            if m:
                return {'initial_value': value,
                        'value': int(m.group('int')),
                        **p.__dict__}
        return {'initial_value': value,
                'value': None}

    @staticmethod
    def cast(value):
        for m in [CInteger._cast]:
            res = m(value)
            if res:
                return res
        return None

    @staticmethod
    def convert_to(value):
        res = CInteger.cast(value)['value']
        if res is not None:
            return int(res)
        return None
