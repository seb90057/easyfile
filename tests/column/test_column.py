import unittest
from easy_file.column.column import Column
import pandas as pd
from pandas.testing import assert_frame_equal
from easy_file.cast.constant.cdate import CDate
from easy_file.cast.constant.cboolean import CBoolean
from easy_file.cast.constant.cinteger import CInteger
from easy_file.cast.constant.cfloat import CFloat
from easy_file.cast.constant.cstring import CString
import datetime


class ColumnTest(unittest.TestCase):
    def setUp(self) -> None:
        value_list = ['2010-04-10', '27/01/1983', '19 04 2015']
        self.column = Column(value_list)

    def test_cast_matrix(self):
        result = self.column.cast_matrix
        expected_result = pd.DataFrame(data = {CBoolean.type: [None, None, None],
                                               CDate.type: [datetime.date(year=2010,
                                                                          month=4,
                                                                          day=10),
                                                            datetime.date(year=1983,
                                                                          month=1,
                                                                          day=27),
                                                            datetime.date(year=2015,
                                                                          month=4,
                                                                          day=19)],
                                               CInteger.type: [None, None, int(19042015)],
                                               CFloat.type: [None, None, float(19042015)],
                                               CString.type: ['2010-04-10', '27/01/1983', '19 04 2015']})
        assert_frame_equal(expected_result, result, check_dtype=False)

    def test_get_cast(self):
        result = self.column.cast
        expected_result = CDate
        self.assertEqual(expected_result, result)

    def test_isolate_field_cast(self):
        result = self.column.isolated_fields
        expected_result = [
            {
                'type': CDate,
                'initial_value': '2010-04-10',
                'value': datetime.date(2010, 4, 10),
                'comment': 'DD-MM-YYYY',
                'pattern': '^(?P<year>[0-9]{2,4})-(?P<month>[0-1]{0,1}[0-9])-(?P<day>[0-3]{0,1}[0-9])$'
            },
            {
                'type': CDate,
                'initial_value': '27/01/1983',
                'value': datetime.date(1983, 1, 27),
                'comment': 'DD/MM/YYYY',
                'pattern': '^(?P<day>[0-3]{0,1}[0-9])/(?P<month>[0-1]{0,1}[0-9])/(?P<year>[0-9]{2,4})$'
            },
            {
                'type': CDate,
                'initial_value': '19 04 2015',
                'value': datetime.date(2015, 4, 19),
                'comment': 'DD MM YYYY',
                'pattern': '^(?P<day>[0-3]{0,1}[0-9]) (?P<month>[0-1]{0,1}[0-9]) (?P<year>[0-9]{2,4})$'
            }
        ]
        self.assertListEqual(expected_result, result)