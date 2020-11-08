from easy_file.cast.cast import cast
import pandas as pd
from easy_file.utils import timeit


class Field:
    # @timeit
    def __init__(self, value):
        self.value = value
        self.cast_priority_list = cast(self.value)

    def get_cast_df(self):
        data = {}
        for c in self.cast_priority_list:
            data[c['type'].type] = [c['value']]
        return pd.DataFrame(data)

    # @timeit
    def get_possible_cast(self):
        return [c['type'] for c in self.cast_priority_list if c['value'] is not None]

    def get_specific_cast(self, cast_cls):
        return [r for r in self.cast_priority_list if r['type'] == cast_cls][0]
