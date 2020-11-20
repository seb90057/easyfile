import random
from easy_file.utils import timeit


class File:
    def __init__(self, path):
        self.path = path
        self.extension = File.get_extension(self.path)
        self.row_number = self.get_row_number()

    @timeit
    def get_row_number(self):
        row_nb = 0
        with open(self.path, 'r', errors="ignore", encoding='utf-8-sig') as f:
            for _ in f:
                row_nb += 1
        return row_nb

    @timeit
    def get_sample(self, excluded=None, line_number=1000):
        lines = []

        values = range(1, self.row_number)

        if excluded:
            values = [i for i in range(1, self.row_number) if i not in excluded]

        if not values:
            return [], []

        if line_number > len(values):
            line_number = len(values)

        indexes = random.sample(values, line_number)
        count = len(indexes)
        with open(self.path, 'r', errors="ignore", encoding='utf-8-sig') as f:
            for i, line in enumerate(f):
                if i in indexes:
                    lines.append(line)
                    count -= 1
                if count == 0:
                    break
        return indexes, lines

    @timeit
    def get_raw_lines(self,
                      excluded=None,
                      line_number=None,
                      exclude_first_line=True):
        lines = {}
        if exclude_first_line:
            start = 1
        else:
            start = 0
        values = range(start, self.row_number)

        if excluded:
            values = [i for i in range(start, self.row_number) if i not in excluded]

        if not values:
            return [], []

        if line_number is None or line_number > len(values):
            indexes = values
        else:
            indexes = random.sample(values, line_number)
        count = len(indexes)
        with open(self.path, 'r', errors="ignore", encoding='utf-8-sig') as f:
            for i, line in enumerate(f):
                if i in indexes:
                    lines[i] = line
                    count -= 1
                if count == 0:
                    break
        return lines


    @timeit
    def get_first_line(self):
        with open(self.path, 'r', errors="ignore", encoding='utf-8-sig') as f:
            return f.readline()

    @staticmethod
    def get_extension(path):
        return path.split(".")[-1]


if __name__ == '__main__':
    import json
    path = r"C:\tmp\data\test2.csv"
    f = File(path)
    res = f.get_raw_lines(excluded=range(1030), line_number=2)
    print(json.dumps(res, indent=4))