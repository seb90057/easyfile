from easy_file.sql.connector import SqlConnector
from easy_file.sql.column import Column


class Table:
    def __init__(self, table_name):
        self.name = table_name
        self.columns = []

    def add_column(self, column):
        if not self.column_exists(column.name):
            self.columns.append(column)

    def add_columns(self, columns):
        for column in columns:
            self.add_column(column)

    def get_column(self, column_name):
        return next((c for c in self.columns if c.name == column_name), None)

    def column_exists(self, column_name):
        if self.get_column(column_name):
            return True
        return False

    def _create_table_request(self):
        column_definition = []
        other_definition = []
        for column in self.columns:
            c_def, o_def = column.get_column_definition()
            column_definition.append(c_def)
            if o_def:
                other_definition.append(o_def)
        column_definition.extend(other_definition)

        request = 'CREATE TABLE IF NOT EXISTS {table_name} (\n' \
                  '{columns}\n' \
                  ');'.format(table_name=self.name,
                              columns=',\n'.join(column_definition))

        return request

    def check_headers(self, headers):
        """
        Check if the header for insert equals to the one define on table
        :param headers: the header used for insert
        :return: True or False
        """
        expected_headers = [c.name for c in self.columns]
        if set(expected_headers) == set(headers):
            return True
        return False

    def _insert_lines_request(self, header_list, values_list):
        if not self.check_headers(header_list):
            raise Exception('the suggested header is different from the one '
                            'defined on table {}'.format(self.name))
        header_request = ','.join(header_list)
        converted_values_list = []
        for values in values_list:
            converted_values = [self.get_column(header_list[i])
                                    .get_request_value(v)
                                for i, v in enumerate(values)]
            converted_values_list.append(converted_values)

        values_request = ',\n'.join(['({})'
                                    .format(','.join([str(v) for v in values]))
                                     for values in converted_values_list])
        request = 'INSERT INTO {name} ({header})\n' \
                  'VALUES\n' \
                  '{values};'.format(name=self.name,
                                     header=header_request,
                                     values=values_request)
        return request

    def set_table(self):
        result = self.get_table_info()

        for column_desc in result:
            column = Column(column_desc['name'], column_desc['type'])
            if column_desc['notnull']:
                column.is_not_null()
            if column_desc['pk']:
                column.is_primary_key()

            self.add_column(column)

    def _get_table_info_request(self):
        """
        Get table infos.
        :return: the result
        """
        request = 'SELECT * FROM PRAGMA_TABLE_INFO("{name}");'\
            .format(name=self.name)

        return request

    def get_lines(self, columns_list=None, conditions=None):
        """
        Get lines.
        :return: the result
        """
        if not columns_list:
            columns_list = ['*']
        request = 'SELECT {columns} FROM {name};'\
            .format(name=self.name, columns=','.join(columns_list))

        header, rows = SqlConnector.execute_request(request)
        return header, rows

    def _get_table_info(self):
        header, rows = SqlConnector.execute_request(self._get_table_info_request())
        return header, rows

    def get_table_info(self):
        header, rows = self._get_table_info()
        result = []
        for r in rows:
            r_dict = {}
            for i, h in enumerate(header):
                r_dict[h] = r[i]
            result.append(r_dict)

        return result

    def create_table(self):
        SqlConnector.execute_request(self._create_table_request())

    def insert_lines(self, header_list, values_list):
        SqlConnector\
            .execute_request(
            self._insert_lines_request(header_list, values_list)
        )


if __name__ == '__main__':
    SqlConnector.get_or_create_connection()
    table = Table('boolean_patterns')
    table.set_table()

    header, rows = table.get_lines()


    print('ok')
