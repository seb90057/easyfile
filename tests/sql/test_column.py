import unittest
from easy_file.sql.column import Column


class ColumnTest(unittest.TestCase):
    def setUp(self) -> None:
        self.column = Column('col_name', 'text')

    def test_is_null(self):
        self.column.is_null()
        self.assertTrue(self.column.null_values)

    def test_is_not_null(self):
        self.column.is_not_null()
        self.assertFalse(self.column.null_values)

    def test_is_primary_key(self):
        self.column.is_primary_key()
        self.assertEqual(self.column.key_type, Column._PRIMARY)
        self.assertIsNone(self.column.foreign_table_name)
        self.assertIsNone(self.column.foreign_column_name)

    def test_is_foreign_key(self):
        self.column.is_foreign_key('table_name', 'column_name')
        self.assertEqual(self.column.key_type, Column._FOREIGN)
        self.assertEqual(self.column.foreign_table_name, 'table_name')
        self.assertEqual(self.column.foreign_column_name, 'column_name')

    def test_is_not_key(self):
        self.column.is_not_key()
        self.assertIsNone(self.column.key_type)
        self.assertIsNone(self.column.foreign_table_name)
        self.assertIsNone(self.column.foreign_column_name)

    def test_get_column_definition(self):
        column_def, other_def = self.column.get_column_definition()
        exp_column_def = 'col_name text'
        self.assertEqual(column_def, exp_column_def)
        self.assertIsNone(other_def)

        self.column.is_primary_key()
        column_def, other_def = self.column.get_column_definition()
        exp_column_def = 'col_name text PRIMARY KEY'
        self.assertEqual(column_def, exp_column_def)
        self.assertIsNone(other_def)

        self.column.is_foreign_key('table_name', 'column_name')
        column_def, other_def = self.column.get_column_definition()
        exp_column_def = 'col_name text'
        exp_other_def = 'FOREIGN KEY (col_name) REFERENCES table_name (column_name)'

        self.assertEqual(column_def, exp_column_def)
        self.assertEqual(other_def, exp_other_def)

    def test_get_request_value(self):
        result = self.column.get_request_value('test')
        expected_result = '"test"'
        self.assertEqual(result, expected_result)

        self.column.type = 'integer'
        result = self.column.get_request_value('test')
        expected_result = 'test'
        self.assertEqual(result, expected_result)


