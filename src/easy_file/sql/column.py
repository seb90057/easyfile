

class Column:

    _PRIMARY = 'PRIMARY'
    _FOREIGN = 'FOREIGN'
    _TYPES = ['null', 'integer', 'real', 'text', 'blob']

    def __init__(self,
                 column_name,
                 column_type):
        self.name = column_name
        self.type = column_type
        self.key_type = None
        self.foreign_table_name = None
        self.foreign_column_name = None
        self.is_null = True

    def is_null(self):
        self.is_null = True

    def is_not_null(self):
        self.is_null = False

    def is_primary_key(self):
        self.key_type = Column._PRIMARY
        self.foreign_table_name = None
        self.foreign_column_name = None

    def is_foreign_key(self, table_reference, column_reference):
        self.key_type = Column._FOREIGN
        self.foreign_table_name = table_reference
        self.foreign_column_name = column_reference

    def is_not_key(self):
        self.key_type = None
        self.foreign_table_name = None
        self.foreign_column_name = None

    def get_column_definition(self):
        column_definition = '{name} {type}'\
            .format(name=self.name,
                    type=self.type)
        other_definition = None
        if self.key_type:
            if self.key_type == Column._PRIMARY:
                column_definition += ' PRIMARY KEY'
            if self.key_type == Column._FOREIGN:
                other_definition = \
                    'FOREIGN KEY ({name}) REFERENCES {table_ref} ({col_ref})'\
                        .format(name=self.name,
                                table_ref=self.foreign_table_name,
                                col_ref=self.foreign_column_name)

        if not self.is_null:
            column_definition += ' NOT NULL'

        return column_definition, other_definition

    def get_request_value(self, value):
        if self.type == 'text':
            return '"{}"'.format(value)
        return value

    def __str__(self):
        res = ['{}: {}'.format(k, v) for k, v in self.__dict__.items()]
        return '\n'.join(res)


if __name__ == '__main__':
    c = Column('toto', 'text')
    c.is_not_null()
    # c.is_primary_key()
    c.is_foreign_key('titi_table', 'titi_column')
    basic_def, addi_def = c.get_column_definition()
    print(basic_def)
    print(addi_def)
    print(c)
