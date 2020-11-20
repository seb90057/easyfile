import re
from easy_file.cast.constant.cglobal import CPattern


class CFloat(CPattern):
    patterns = None
    type = 'FLOAT'
    patterns_table = 'float_patterns'

    @staticmethod
    def _cast(value):
        v = value.replace(' ', '')
        CFloat.patterns = CFloat.get_or_create_patterns()
        for p in CFloat.patterns:
            m = re.match(p['pattern'], v)
            if m:
                i = m.group('int')
                if i is None:
                    i = '0'
                d = m.group('dec')
                if d is None:
                    d = '0'
                return {'initial_value': value,
                        'value': float('{}.{}'.format(i, d)),
                        **p}
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
