import unittest
from easy_file.cast.constant.cfloat import CFloat
from unittest.mock import MagicMock


class CFloatTest(unittest.TestCase):

    data = [
        {'value': 1.3,
         'comment': 'xxx,xxx',
         'initial_value': '1, 3',
         'pattern': '^(?P<int>[-+]?[0-9]*)(,(?P<dec>[0-9]*))?$'},
        {'value': None,
         'initial_value': 'toto'}
    ]

    def setUp(self) -> None:
        float_patterns = [
            {'pattern': '^(?P<int>[-+]?[0-9]*)(,(?P<dec>[0-9]*))?$',
             'comment': 'xxx,xxx'}
        ]
        CFloat.get_or_create_patterns = MagicMock(return_value=float_patterns)

    def test_cast(self):
        for t in CFloatTest.data:
            expected_result = {**t}
            result = CFloat.cast(t['initial_value'])
            self.assertDictEqual(expected_result, result)

    def test_convert_to(self):
        for t in CFloatTest.data:
            expected_result = t['value']
            result = CFloat.convert_to(t['initial_value'])
            self.assertEqual(expected_result, result)