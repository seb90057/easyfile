import unittest
from easy_file.cast.constant.cinteger import CInteger
from unittest.mock import MagicMock


class CIntegerTest(unittest.TestCase):

    data = [
        {'value': 1,
         'comment': 'xxx,0',
         'initial_value': '1, 0',
         'pattern': '^(?P<int>[-+]?[0-9]+)(,0*)?$'},
        {'value': None,
         'initial_value': 'toto'}
    ]

    def setUp(self) -> None:
        integer_patterns = [
            {'pattern': '^(?P<int>[-+]?[0-9]+)(,0*)?$',
             'comment': 'xxx,0'}
        ]
        CInteger.get_or_create_patterns = MagicMock(return_value=integer_patterns)

    def test_cast(self):
        for t in CIntegerTest.data:
            expected_result = {**t}
            result = CInteger.cast(t['initial_value'])
            self.assertDictEqual(expected_result, result)

    def test_convert_to(self):
        for t in CIntegerTest.data:
            expected_result = t['value']
            result = CInteger.convert_to(t['initial_value'])
            self.assertEqual(expected_result, result)