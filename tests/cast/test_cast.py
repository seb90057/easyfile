import unittest
from easy_file.cast.cast import cast
from easy_file.cast.constant.cdate import CDate
from easy_file.cast.constant.cboolean import CBoolean
from easy_file.cast.constant.cinteger import CInteger
from easy_file.cast.constant.cfloat import CFloat
from easy_file.cast.constant.cstring import CString
import datetime


class CastTest(unittest.TestCase):
    data = [
        {
            'type': CBoolean,
            'value': None,
            'initial_value': '27/01/1983'
        },
        {
            'type': CDate,
            'value': datetime.date(year=1983,
                                   month=1,
                                   day=27),
            'comment': 'DD/MM/YYYY',
            'initial_value': '27/01/1983',
            'pattern': '^(?P<day>[0-3]{0,1}[0-9])/(?P<month>[0-1]{0,1}[0-9])/(?P<year>[0-9]{2,4})$'
        },
        {
            'type': CInteger,
            'value': None,
            'initial_value': '27/01/1983'
        },
        {
            'type': CFloat,
            'value': None,
            'initial_value': '27/01/1983'
        },
        {
            'type': CString,
            'value': '27/01/1983',
            'initial_value': '27/01/1983',
            'comment': 'string',
            'pattern': '^.*$'
        }
    ]

    def test_cast(self):
        result = cast('27/01/1983')
        self.assertListEqual(CastTest.data, result)
