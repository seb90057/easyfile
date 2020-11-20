import unittest
from easy_file.cast.constant.cboolean import CBoolean
from unittest.mock import MagicMock


class CBooleanTest(unittest.TestCase):
    def setUp(self) -> None:
        patterns = [
            {'pattern': '^(?P<true>true)|(?P<false>false)$',
             'comment': 'true/false'}
        ]
        CBoolean.get_or_create_patterns = MagicMock(return_value=patterns)

    def test_cast(self):
        value = 'true'
        expected_result = {'initial_value': value,
                           'value': True,
                           'comment': 'true/false',
                           'pattern': '^(?P<true>true)|(?P<false>false)$'}
        result = CBoolean.cast(value)
        self.assertDictEqual(expected_result, result)

        value = '19 04 2015'
        expected_result = {'initial_value': value,
                           'value': None}
        result = CBoolean.cast(value)
        self.assertDictEqual(expected_result, result)

    def test_convert_to(self):
        value = 'true'
        expected_result = True
        result = CBoolean.convert_to(value)
        self.assertEqual(expected_result, result)

        value = 'toto'
        expected_result = None
        result = CBoolean.convert_to(value)
        self.assertEqual(expected_result, result)
