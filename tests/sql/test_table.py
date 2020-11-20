import unittest
from easy_file.sql.table import Table
from easy_file.sql.column import Column
from unittest.mock import MagicMock


class TableTest(unittest.TestCase):
    def setUp(self) -> None:
        self.table = Table('table_name')
        self.column_1 = Column('col_name_1', 'text')
        self.column_2 = Column('col_name_2', 'integer')

        rv = (
            ['name', 'type', 'notnull', 'pk'],
            [
                ('pattern', 'text', 0, 1),
                ('comment', 'text', 0, 0)]
        )

        self.table._get_table_info = MagicMock(return_value=rv)

    def test_add_column(self):
        self.table.add_column(self.column_1)
        self.assertIn(self.column_1, self.table.columns)

    def test_add_columns(self):
        self.table.add_columns([self.column_1, self.column_2])
        self.assertIn(self.column_1, self.table.columns)
        self.assertIn(self.column_2, self.table.columns)

    def test_get_column(self):
        self.table.add_column(self.column_1)
        result = self.table.get_column('col_name_1')
        expected_result = self.column_1
        self.assertEqual(result, expected_result)

        result = self.table.get_column('col_name_2')
        self.assertIsNone(result)

    def test_column_exists(self):
        self.table.add_column(self.column_1)

        result = self.table.column_exists('col_name_1')
        self.assertTrue(result)

        result = self.table.column_exists('col_name_2')
        self.assertFalse(result)

    def test__create_table_request(self):
        self.table.add_column(self.column_1)
        self.table.add_column(self.column_2)
        request = self.table._create_table_request()
        expected_request = 'CREATE TABLE IF NOT EXISTS table_name (\n' \
                           'col_name_1 text,\n' \
                           'col_name_2 integer\n' \
                           ');'
        self.assertEqual(request, expected_request)

    def test_check_headers(self):
        self.table.add_column(self.column_1)
        self.table.add_column(self.column_2)
        header = ['col_name_2', 'col_name_1']
        result = self.table.check_headers(header)
        self.assertTrue(result)

        header = ['col_name_2', 'col_name_7']
        result = self.table.check_headers(header)
        self.assertFalse(result)

    def test__insert_lines_request(self):
        self.table.add_column(self.column_1)
        self.table.add_column(self.column_2)

        header = ['col_name_1', 'col_name_2']
        values = [
            ['a', 1],
            ['b', 2]
        ]
        result = self.table._insert_lines_request(header, values)
        expected_result = 'INSERT INTO table_name (col_name_1,col_name_2)\n' \
                          'VALUES\n' \
                          '("a",1),\n' \
                          '("b",2);'
        self.assertEqual(result, expected_result)

        header = ['col_name_1']
        values = [
            ['a'],
            ['b']
        ]
        exception_message = 'the suggested header is different from the one ' \
                            'defined on table {}'.format(self.table.name)
        with self.assertRaises(Exception) as context:
            self.table._insert_lines_request(header, values)
        self.assertEqual(exception_message, str(context.exception))

    def test_get_table_info(self):
        result = self.table.get_table_info()
        expected_result = [{'name': 'pattern', 'type': 'text', 'notnull': 0, 'pk': 1}, {'name': 'comment', 'type': 'text', 'notnull': 0, 'pk': 0}]
        self.assertListEqual(result, expected_result)

    def test_set_table(self):
        self.table.set_table()

        self.assertIsNotNone(self.table.get_column('pattern'))
        self.assertIsNotNone(self.table.get_column('comment'))

        self.assertEqual(len(self.table.columns), 2)

        col_pattern = self.table.get_column('pattern')
        self.assertEqual(col_pattern.type, 'text')
        self.assertEqual(col_pattern.key_type, Column._PRIMARY)
        self.assertTrue(col_pattern.null_values)

        col_pattern = self.table.get_column('comment')
        self.assertEqual(col_pattern.type, 'text')
        self.assertIsNone(col_pattern.key_type)
        self.assertTrue(col_pattern.null_values)
