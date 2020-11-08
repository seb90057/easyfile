from easy_file.cast.constant.cboolean import CBoolean
from easy_file.cast.constant.cdate import CDate
from easy_file.cast.constant.cfloat import CFloat
from easy_file.cast.constant.cinteger import CInteger
from easy_file.cast.constant.cstring import CString
from easy_file.utils import timeit

_TYPE_PRIORITY = [CBoolean,
                  CDate,
                  CInteger,
                  CFloat,
                  CString]


# @timeit
def cast(value):
    """
    get a dict with cast type as value and casted value as value
    :param val:
    :return:
    """
    row = []
    for m in _TYPE_PRIORITY:
        v = m.cast(value)
        row.append({'type': m,
                    **v})
    return row
