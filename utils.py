from datetime import datetime
from functools import wraps
import pandas as pd
import threading


class convert_utils:
    """
    This class provides utility functions that could be used to convert
    various inputs to desired types
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def list_of_dicts_to_dict(list_dicts):
        """Converts a list of dictionaries with similar structure to a single dict with all values in appended in a
        single list value """
        flat_dict = dict()
        keys = list_dicts[0].keys()
        for key in keys:
            values = []
            [values.append(list_dicts[i].get(key)) for i in range(len(list_dicts))]
            flat_dict.update({key: values})

        return flat_dict

    @staticmethod
    def df_list_column_to_multi(df_with_list):
        """
        If any column in the input dataframe is a list, this function breaks it to multi columns with
        single value in them. For example, if column includes a list [a ,b]", this function creates two columns,
        one for item a and one for item b
        """
        dict_column = dict()

        for i in range(df_with_list.shape[1]):
            if isinstance(df_with_list.iloc[0, i], list):
                column_name = df_with_list.columns[i]
                for _ in range(len(df_with_list.iloc[0, i])):
                    key = column_name + str(_)
                    # dict_column.keys() = key_val
                    values = []
                    [values.append(df_with_list.iloc[j, i][_]) for j in range(df_with_list.shape[0])]
                    dict_column.update({key: values})
        df_dict = pd.DataFrame.from_dict(dict_column)
        df_with_list = pd.concat([df_with_list, df_dict], axis=1)

        return df_with_list


def add_time(df):
    """Adds a "time" column to a dataframe, which includes the instant time"""
    if isinstance(df, pd.DataFrame):
        df['time'] = datetime.now()
    else:
        raise TypeError("The input should be of type Dataframe")


def run_in_thread(fn):
    """This decorator executes a function in a Thread"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
