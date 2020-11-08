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
            return None, None

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
    def get_first_line(self):
        with open(self.path, 'r', errors="ignore", encoding='utf-8-sig') as f:
            return f.readline()

    @staticmethod
    def get_extension(path):
        return path.split(".")[-1]


if __name__ == "__main__":
    # input_path = 'C:/tmp/data/clean.csv'
    # input_path = r"C:\tmp\data\CORD-19-research-challenge\cord_19_embeddings\cord_19_embeddings_2020-05-19.csv"
    # f = File(input_path)
    # print(f.row_number)
    # lines = f.get_sample()
    l = []
    if not l:
        print('OK')
