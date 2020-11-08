import re
from easy_file.cast.patterns.c_patterns import CPattern


class CFloat:
    patterns = None
    type = 'FLOAT'
    patterns_table = 'float_patterns'

    @staticmethod
    def _cast(value):
        v = value.replace(' ', '')
        CFloat.patterns = CPattern.get_patterns(CFloat.patterns_table)
        for p in CFloat.patterns:
            m = re.match(p.pattern, v)
            if m:
                i = m.group('int')
                if i is None:
                    i = '0'
                d = m.group('dec')
                if d is None:
                    d = '0'
                return {'initial_value': value,
                        'value': float('{}.{}'.format(i, d)),
                        **p.__dict__}
        return {'initial_value': value,
                'value': None}

    @staticmethod
    def cast(value):
        for m in [CFloat._cast]:
            res = m(value)
            if res:
                return res
        return None

    @staticmethod
    def convert_to(value):
        res = CFloat.cast(value)['value']
        if res is not None:
            return float(res)
        return None
