import pandas as pd
from functools import wraps
import time
import utils
from utils import convert_utils as cu
from datetime import datetime


class tables:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_table(data):
        """Creates a data frame with a list including the columns names as input """
        import pandas as pd
        if isinstance(data, list):
            if isinstance(data[0], dict):
                dict_data = cu.list_of_dicts_to_dict(data)
                df = pd.DataFrame.from_dict(dict_data)
            else:
                df = pd.DataFrame(columns=data)
        elif isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
        else:
            raise TypeError("Input data type is not acceptable, only 'list' and 'dict' types are acceptable")
        return df

    def continuous_data_collector(func):
        """This wrapper continuously collects data from API"""

        @wraps(func)
        def wrapper(self, freq, periods, limit, end_time, add_time, csv_name):
            if periods and end_time:
                raise InterruptedError("Either periods or end_time should be specified")
            df = pd.DataFrame()
            if periods:
                for _ in range(periods):
                    df_ = func(self, freq, periods, limit)
                    if add_time:
                        utils.add_time(df_)
                    frames = [df, df_]
                    df = pd.concat(frames, ignore_index=True)
                    if csv_name:
                        df.to_csv(f"{csv_name}.csv", index=False)
                    time.sleep(freq)

            if end_time:
                end_time_object = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                if datetime.now() > end_time_object:
                    raise InterruptedError("end_time cannot be in the past")
                while datetime.now() < end_time_object:
                    df_ = func(self, freq, periods,limit)
                    if add_time:
                        utils.add_time(df_)
                    frames = [df, df_]
                    df = pd.concat(frames, ignore_index=True)
                    if csv_name:
                        df.to_csv(f"{csv_name}.csv", index=False)
                    time.sleep(freq)
            return df

        return wrapper
