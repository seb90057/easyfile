import unittest
from easy_file.cast.cast import cast
from easy_file.cast.constant.cdate import CDate
from easy_file.cast.constant.cboolean import CBoolean
from easy_file.cast.constant.cinteger import CInteger
from easy_file.cast.constant.cfloat import CFloat
from easy_file.cast.constant.cstring import CString
import datetime
from unittest.mock import MagicMock


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

    def setUp(self) -> None:
        boolean_patterns = [
            {'pattern': '^(?P<true>true)|(?P<false>false)$',
             'comment': 'true/false'}
        ]
        CBoolean.get_or_create_patterns = MagicMock(return_value=boolean_patterns)

        date_patterns = [
            {'pattern': '^(?P<day>[0-3]{0,1}[0-9]) (?P<month>[0-1]{0,1}[0-9]) (?P<year>[0-9]{2,4})$',
             'comment': 'DD MM YYYY'},
            {'pattern': '^(?P<day>[0-3]{0,1}[0-9])/(?P<month>[0-1]{0,1}[0-9])/(?P<year>[0-9]{2,4})$',
             'comment': 'DD/MM/YYYY'}
        ]
        CDate.get_or_create_patterns = MagicMock(return_value=date_patterns)

        float_patterns = [
            {'pattern': '^(?P<int>[-+]?[0-9]*)(\.(?P<dec>[0-9]*))?$',
             'comment': 'xxx.xxx'}
        ]
        CFloat.get_or_create_patterns = MagicMock(return_value=float_patterns)

        integer_patterns = [
            {'pattern': '^(?P<int>[-+]?[0-9]+)(\.0*)?$',
             'comment': 'xxx.0'}
        ]
        CInteger.get_or_create_patterns = MagicMock(return_value=integer_patterns)

        string_patterns = [
            {'pattern': '^.*$',
             'comment': 'string'}
        ]
        CString.get_or_create_patterns = MagicMock(
            return_value=string_patterns)

    def test_cast(self):
        result = cast('27/01/1983')
        self.assertListEqual(CastTest.data, result)
