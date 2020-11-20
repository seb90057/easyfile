import time
import random
import operator
import subprocess
import pkg_resources
import json

method_time = {}


def get_or_create_patterns(cast_cls):
    if cast_cls.patterns is None:
        pkg = 'easy_file.cast.patterns_data'
        r = pkg_resources.resource_filename(pkg, cast_cls.patterns_file_name)
        with open(r, 'r') as patterns_file:
            cast_cls.patterns = json.load(patterns_file)

    return cast_cls.patterns


def get_method_time():
    global method_time
    res = {k: sum(v) for k, v in method_time.items()}
    return res


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        global method_time

        method_name = method.__name__
        if method_name in method_time:
            method_time[method_name].append(te - ts)
        else:
            method_time[method_name] = [te - ts]

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


@timeit
def get_list_sample(l, sample_nb):
    return random.sample(l, sample_nb)


@timeit
def from_row_to_col(row_list):
    res = [[] for col in row_list[0]]
    for row in row_list:
        for i, elt in enumerate(row):
            res[i].append(elt)
    return res

@timeit
def get_col_number(row_list):
    row_len_dict = {}
    for row in row_list:
        row_len = len(row)
        if row_len in row_len_dict:
            row_len_dict[row_len] += 1
        else:
            row_len_dict[row_len] = 1
    print(row_len_dict)
    return max(row_len_dict.items(), key=operator.itemgetter(1))[0]


def get_col_size(vd):
    return max(vd.items(), key=operator.itemgetter(1))[0]


def get_line_discrepancies(df1, df2):

    df1_empty = df1[(df1[df1.columns[0]].isnull()) | (df1[df1.columns[0]] == '')]
    df2_empty = df2[(df2[df2.columns[0]].isnull()) | (df2[df2.columns[0]] == '')]

    df1_null_index = list(df1_empty.index.values)
    df2_null_index = list(df2_empty.index.values)

    difference = set(df1_null_index).symmetric_difference(set(df2_null_index))
    list_difference = list(difference)

    return list_difference


if __name__ == '__main__':
    import pandas as pd
    df1 = pd.DataFrame([(1, 2), (3, '')], columns=['h1', 'h2'])
    df2 = pd.DataFrame([(3, None), ('3', None)], columns=['h1', 'h2'])

    ld = get_line_discrepancies(df1[['h2']], df2[['h2']])
    print(ld)
    print(df1.iloc[ld])
