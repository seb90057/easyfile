import re
from easy_file.cast.patterns.c_patterns import CPattern


class CString:
    patterns = None
    type = 'STRING'
    patterns_table = 'string_patterns'

    @staticmethod
    def _cast(value):
        CString.patterns = CPattern.get_patterns(CString.patterns_table)
        for p in CString.patterns:
            m = re.match(p.pattern, value)
            if m:
                return {'initial_value': value,
                        'value': m.group(),
                        **p.__dict__}
            else:
                continue
        return {'initial_value': value,
                'value': None}

    @staticmethod
    def cast(value):
        for m in [CString._cast]:
            res = m(value)
            if res:
                return res
        return None

    @staticmethod
    def convert_to(value):
        res = CString.cast(value)['value']
        if res is not None:
            return res
        return None
