from easy_file.sql.table import Table
from easy_file.sql.connector import SqlConnector


class CPattern:

    def __init__(self):
        pass

    @staticmethod
    def get_patterns(table_name):
        patterns = []
        pattern_table = Table(table_name)
        header, rows = pattern_table.get_lines()

        for row in rows:
            new_pattern = CPattern()
            for i, h in enumerate(header):
                new_pattern.__dict__[h] = row[i]
            patterns.append(new_pattern)

        return patterns
