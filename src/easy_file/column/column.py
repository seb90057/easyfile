from easy_file.field.field import Field
import pandas as pd
from easy_file.cast.cast import _TYPE_PRIORITY
from easy_file.utils import timeit, get_method_time
import time


class Column:
    @timeit
    def __init__(self, value_list):
        self.field_list = [Field(value) for value in value_list]
        self.cast_matrix = self.get_cast_matrix()
        self.cast = self.get_cast()
        self.isolated_fields = self.isolate_field_cast()

    def isolate_field_cast(self):
        return [f.get_specific_cast(self.cast) for f in self.field_list]

    # @timeit
    def get_cast_matrix(self):
        df_list = []
        for field in self.field_list:
            df_list.append(field.get_cast_df())

        res = pd.concat(df_list, ignore_index=True)
        return res.where(pd.notnull(res), None)

    # @timeit
    def get_cast(self):
        c_df = self.cast_matrix[self.cast_matrix['STRING'].notnull()]
        expected_result_nb = len(c_df.index)

        for cast_object in _TYPE_PRIORITY:
            # get the number of not null row for this cast
            tmp_df = c_df[c_df[cast_object.type].notnull()]
            if expected_result_nb == len(tmp_df.index):
                return cast_object
