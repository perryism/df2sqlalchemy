import numpy as np
from sqlalchemy import Table, Column, Integer, String, Text, MetaData, Float

def load_model_from_dataframe(name, df, primary_keys=None, type_map = {}):
    metadata = MetaData()

    columns = []
    for column, dtype in zip(df.columns, df.dtypes):
        column_type = type_map.get(column)

        if column_type is None:
            if np.issubdtype(dtype, np.float64):
                column_type = Float
            elif np.issubdtype(dtype, np.int64):
                column_type = Integer
            elif np.issubdtype(dtype, np.object):
                column_type = String  # Text??
            else:
                raise "Unsupported dtype %s"%dtype

        columns.append(Column(column, column_type, primary_key=(column in primary_keys)))
    args = [name, metadata] + columns

    return Table(*args)
