import re
from easy_file.cast.patterns.c_patterns import CPattern


class CBoolean:
    patterns = None
    type = 'BOOLEAN'
    patterns_table = 'boolean_patterns'

    @staticmethod
    def cast(value):
        for m in [CBoolean._cast]:
            res = m(value)
            if res is not None:
                return res
        return None

    @staticmethod
    def _cast(value):
        v = value.replace(' ', '').lower()
        CBoolean.patterns = CPattern.get_patterns(CBoolean.patterns_table)
        for p in CBoolean.patterns:
            m = re.match(p.pattern, v)
            if m is None:
                continue
            t = m.group('true')
            f = m.group('false')

            if t:
                res = True
            else:
                res = False
            return {'initial_value': value,
                    'value': res,
                    **p.__dict__}
        return {'initial_value': value,
                'value': None}

    @staticmethod
    def convert_to(value):
        res = CBoolean.cast(value)['value']
        if res is not None:
            return res
        return None
