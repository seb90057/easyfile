import unittest
from easy_file.cast.constant.cstring import CString


class CStringTest(unittest.TestCase):

    data = [
        {'value': '1, 0',
         'comment': 'string',
         'initial_value': '1, 0',
         'pattern': '^.*$'}
    ]

    def test_cast(self):
        for t in CStringTest.data:
            expected_result = {**t}
            result = CString.cast(t['initial_value'])
            self.assertDictEqual(expected_result, result)

    def test_convert_to(self):
        for t in CStringTest.data:
            expected_result = t['value']
            result = CString.convert_to(t['initial_value'])
            self.assertEqual(expected_result, result)