import unittest
from easy_file.cast.utils import test_pattern, get_group
import re


class UtilsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pattern = '[0-9]{2}(?P<test_group>toto)'
        self.value = '01toto'
        self.m = re.match(self.pattern, self.value)

    def test_test_pattern(self):
        result = test_pattern(self.pattern, self.value)

        expected_result = {'match': True,
                           'groups':
                               {'test_group': 'toto'}
                           }
        self.assertDictEqual(result, expected_result)

        value = 'test'
        result = test_pattern(self.pattern, value)

        expected_result = {'match': False,
                           'groups': {}
                           }
        self.assertDictEqual(result, expected_result)

    def test_get_group(self):
        result = get_group(self.m, 'test_group')
        expected_result = 'toto'
        self.assertEqual(result, expected_result)

        result = get_group(self.m, 'no_group')
        self.assertIsNone(result)
