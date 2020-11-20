import unittest
from unittest.mock import MagicMock
from easy_file.sql.connector import SqlConnector


class ConnectorTest(unittest.TestCase):
    def setUp(self) -> None:
        SqlConnector.get_or_create_connection = MagicMock(return_value=True)
        SqlConnector.execute_request = MagicMock(return_value=
                                                 (
                                                     ['h1', 'h2'],
                                                     [('a', 'b'),
                                                      ('c', 'd')]
                                                 ))

    def test_get_or_create_connection(self):
        self.assertTrue(SqlConnector.get_or_create_connection())

    def test_execute_request(self):
        header, rows = SqlConnector.execute_request()
        self.assertListEqual(header, ['h1', 'h2'])
        self.assertListEqual(rows, [('a', 'b'), ('c', 'd')])
