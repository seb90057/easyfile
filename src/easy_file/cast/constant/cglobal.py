from easy_file.sql.table import Table

_GET = 0
_CREATE = 0


class CPattern:
    patterns = None
    patterns_table = None

    @classmethod
    def get_or_create_patterns(cls):
        if cls.patterns:
            return cls.patterns
        else:
            patterns = []
            pt = Table(cls.patterns_table)
            header, rows = pt.get_lines()

            for row in rows:
                new_pattern = {}
                for i, h in enumerate(header):
                    new_pattern[h] = row[i]
                patterns.append(new_pattern)
            cls.patterns = patterns
            return patterns
