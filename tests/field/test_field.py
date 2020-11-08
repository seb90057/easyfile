import unittest
from easy_file.field.field import Field
import pandas as pd
from pandas.testing import assert_frame_equal
from easy_file.cast.constant.cdate import CDate
from easy_file.cast.constant.cboolean import CBoolean
from easy_file.cast.constant.cinteger import CInteger
from easy_file.cast.constant.cfloat import CFloat
from easy_file.cast.constant.cstring import CString
import datetime


class FieldTest(unittest.TestCase):

    df_desc = {CBoolean.type: [None],
               CDate.type: [datetime.date(year=1983,
                                month=1,
                                day=27)],
               CInteger.type: [27011983],
               CFloat.type: [float(27011983)],
               CString.type: ['27 01 1983']}

    @staticmethod
    def test_get_cast_df():
        f = Field('27 01 1983')
        result = f.get_cast_df()
        expected_result = pd.DataFrame(data=FieldTest.df_desc)
        assert_frame_equal(result, expected_result)

    def test_get_specific_cast(self):
        f = Field('27 01 1983')
        result = f.get_specific_cast(CDate)
        expected_result = {'type': CDate,
                           'initial_value': '27 01 1983',
                           'value': datetime.date(1983, 1, 27),
                           'comment': 'DD MM YYYY',
                           'pattern': '^(?P<day>[0-3]{0,1}[0-9]) (?P<month>[0-1]{0,1}[0-9]) (?P<year>[0-9]{2,4})$'}
        self.assertDictEqual(expected_result, result)
