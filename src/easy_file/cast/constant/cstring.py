import re
from easy_file.cast.constant.cglobal import CPattern


class CString(CPattern):
    patterns = None
    type = 'STRING'
    patterns_table = 'string_patterns'

    @staticmethod
    def _cast(value):
        CString.patterns = CString.get_or_create_patterns()
        for p in CString.patterns:
            m = re.match(p['pattern'], value)
            if m:
                return {'initial_value': value,
                        'value': m.group(),
                        **p}
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
