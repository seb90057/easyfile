import unittest
from easy_file.cast.constant.cglobal import CPattern
from easy_file.cast.constant.cboolean import CBoolean
from unittest.mock import MagicMock


class CPatternTest(unittest.TestCase):
    def setUp(self) -> None:
        self.patterns = [
            {'pattern': '^(?P<true>true)|(?P<false>false)$',
             'comment': 'true/false'}
        ]
        CBoolean.get_or_create_patterns = MagicMock(return_value=self.patterns)

    def test_get_or_create_pattern(self):
        self.assertListEqual(self.patterns, CBoolean.get_or_create_patterns())

