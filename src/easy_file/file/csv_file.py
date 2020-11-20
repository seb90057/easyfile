import csv
import pandas as pd
from easy_file.file.file import File
from easy_file.utils import timeit, \
    from_row_to_col,\
    get_line_discrepancies
from easy_file.column.column import Column
from easy_file.field.field import Field
import operator


class CsvFile(File):

    extension = ['csv']

    @timeit
    def __init__(self, path):
        super().__init__(path)
        self.dialect = None
        self.delimiter = None
        self.quotechar = None
        self.escapechar = None
        self.has_header = None
        self.headers = None
        self.headers_cast = None
        self.df = None
        self.lines = None
        self.bad_lines = None

    @timeit
    def get_headers(self):
        if not self.headers:
            self.set_columns_charac()
        return self.headers

    @timeit
    def get_headers_cast(self):
        if not self.headers_cast:
            self.set_columns_charac()
        return self.headers_cast

    @timeit
    def set_dialect(self):
        if not self.dialect:
            sniffer = csv.Sniffer()
            csv_file_dict = self.get_raw_lines(line_number=1000)
            csv_file_sample = csv_file_dict.values()
            self.dialect = sniffer.sniff("\n".join(csv_file_sample))
            self.delimiter = self.dialect.delimiter
            self.quotechar = self.dialect.quotechar
            self.escapechar = self.dialect.escapechar

    @timeit
    def set_columns_charac(self):
        self.set_dialect()
        _, csv_file_sample = self.get_sample(line_number=100)
        lines_sample = list(csv.reader(csv_file_sample, dialect=self.dialect))
        expected_col_nb = self.get_expected_column_number(lines_sample)
        first_row = list(csv.reader([self.get_first_line()], dialect=self.dialect))[0]
        other_rows = [row for row in lines_sample if len(row) == expected_col_nb]
        other_cols = from_row_to_col(other_rows)

        columns = [Column(oc) for oc in other_cols]
        headers_cast = [{'type': c.cast} for c in columns]

        if len(first_row) != expected_col_nb:
            self.headers = ['header_{}'.format(i) for i in range(expected_col_nb)]
            self.has_header = False
        else:
            equal_cast = 0
            first_row_cast = [Field(h).get_possible_cast() for h in first_row]
            for i, frc_list in enumerate(first_row_cast):
                other_rows_cast_type = headers_cast[i]['type']
                if other_rows_cast_type.type in [frc.type for frc in frc_list]:
                    equal_cast += 1
            if equal_cast == len(first_row):
                self.headers = ['header_{}'.format(i) for i in
                                range(expected_col_nb)]
                self.has_header = False
            else:
                self.headers = first_row
                self.has_header = True

        self.headers_cast = {}
        for i, h in enumerate(self.headers):
            self.headers_cast[h] = headers_cast[i]

    @timeit
    def get_lines(self):
        if self.lines:
            return self.lines
        self.set_dialect()
        good_lines = {}
        with open(self.path, 'r', errors="ignore", encoding='utf-8-sig') as f:
            csv_reader = csv.reader(f, dialect=self.dialect)
            headers = self.get_headers()
            for i, row in enumerate(csv_reader):
                if len(row) == len(headers):
                    good_lines[i] = row
                else:
                    self.add_bad_line(i, row, 'column number')
        if self.has_header:
            del good_lines[0]

        self.lines = good_lines
        return self.lines

    @timeit
    def get_or_create_df(self):
        if not self.headers:
            self.set_columns_charac()
        if self.df is not None:
            return self.df
        else:
            row_dict = self.get_raw_lines()
            headers = ['line_number']
            headers.extend(self.headers)
            values = [[k, *v] for k, v in row_dict.items()]
            res = pd.DataFrame(values, columns=headers)
            self.df = res
            return self.df

    @timeit
    def get_or_create_df(self):
        if not self.headers:
            self.set_columns_charac()
        if self.df is not None:
            return self.df
        else:
            row_dict = self.get_lines()
            headers = ['line_number']
            headers.extend(self.headers)
            values = [[k, *v] for k, v in row_dict.items()]
            res = pd.DataFrame(values, columns=headers)
            self.df = res
            return self.df

    @timeit
    def get_converted_df(self, line_number=None):
        if line_number:
            df = self.get_sample_df(line_number=line_number)
        else:
            df = self.get_or_create_df()
        res = pd.DataFrame()
        header_dict = self.get_headers_cast()

        indexes_to_exclude = []

        res['line_number'] = df['line_number']

        for header, header_cast in header_dict.items():
            res[header] = df[header].apply(lambda row: header_cast['type'].convert_to(row))
            indexes_to_exclude.extend(get_line_discrepancies(df[[header]], res[[header]]))

        to_exclude = res.index.isin(list(set(indexes_to_exclude)))
        bad_rows = res.loc[to_exclude, :]
        for i, bad_line in bad_rows.iterrows():
            self.add_bad_line(bad_line['line_number'], list(bad_line), 'cast')

        return res[~to_exclude], res[to_exclude]

    def get_expected_column_number(self, lines_sample):
        if self.headers:
            return len(self.headers)
        res = {}
        for line in lines_sample:
            line_size = len(line)
            if line_size in res:
                res[line_size] += 1
            else:
                res[line_size] = 1
        return max(res.items(), key=operator.itemgetter(1))[0]

    @timeit
    def get_sample_df(self, line_number=1000):
        if not self.headers:
            self.set_columns_charac()

        indexes, line_list = self.get_sample(line_number=line_number)
        excluded_indexes = []

        good_lines = []
        good_lines_nb = 0
        res_nb = len(line_list)

        while good_lines_nb <= line_number and res_nb != 0:
            excluded_indexes.extend(indexes)
            for i, line in enumerate(line_list):
                good_line = self.is_good_line(line)
                if good_line:
                    good_lines.append([indexes[i], *good_line])
            good_lines_nb = len(good_lines)
            remaining_line_number = line_number - good_lines_nb
            indexes, line_list = self.get_sample(excluded=excluded_indexes,
                                                 line_number=remaining_line_number)
            res_nb = len(line_list)
        return pd.DataFrame(good_lines, columns=['line_number', *self.headers])

    def is_good_line(self, line):
        if self.dialect is None:
            self.set_dialect()
        if self.headers is None:
            self.get_headers()

        row = next(csv.reader([line], dialect=self.dialect))
        if len(row) != len(self.headers):
            return None
        return row

    def add_bad_line(self, i, row, message):
        if self.bad_lines is None:
            self.bad_lines = {}
        if i in self.bad_lines.keys():
            if message not in self.bad_lines[i]['issue']:
                self.bad_lines[i]['issue'].append(message)
        else:
            self.bad_lines[i] = {'issue': [message],
                                 'row': row}




if __name__ == '__main__':
    from easy_file.cast.constant.cinteger import CInteger
    csv_file = CsvFile(r"C:\tmp\data\test2.csv")
    csv_file.set_dialect()
    csv_file.set_columns_charac()
    cdf, _ = csv_file.get_converted_df(line_number=10)

    print(cdf)


    exit()

    bad_col = [{k: v['row']} for k, v in csv_file.bad_lines.items() if 'column number' in v['issue']]
    bad_cast = [{k: v['row']} for k, v in csv_file.bad_lines.items() if 'cast' in v['issue']]

    print(csv_file.row_number)
