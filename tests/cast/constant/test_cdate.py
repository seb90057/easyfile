import unittest
from easy_file.cast.constant.cdate import CDate
import datetime


class CDateTest(unittest.TestCase):

    data = [
        {'value': datetime.date(year=1983,
                                month=1,
                                day=27),
         'comment': 'DD MM YYYY',
         'initial_value': '27 01 1983',
         'pattern': '^(?P<day>[0-3]{0,1}[0-9]) (?P<month>[0-1]{0,1}[0-9]) (?P<year>[0-9]{2,4})$'},
        {'value': None,
         'initial_value': 'toto'}
    ]

    def test_cast(self):
        for t in CDateTest.data:
            expected_result = {**t}
            result = CDate.cast(t['initial_value'])
            self.assertDictEqual(expected_result, result)

    def test_convert_to(self):
        for t in CDateTest.data:
            expected_result = t['value']
            result = CDate.convert_to(t['initial_value'])
            self.assertEqual(expected_result, result)
