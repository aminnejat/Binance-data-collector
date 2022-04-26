import dataclasses
from binance import Client
from data_utils import tables
from datetime import datetime
from utils import convert_utils as cu
import utils as ut


def timestamp(time):
    """Return second timestamp of date-time format"""
    return round(datetime.timestamp(time))


@dataclasses.dataclass(init=True)
class Binance_data:
    """ Collecting data from Binance

    This class includes methods to collect various data from Binance.
    These data are saved in Dataframes. The instances to this class are api_key,
    api_secret (which can be collected from https://www.binance.com developers' page)
    and symbol, which by default is BTCUSDT. A currency pair is attached to each object of class.

    """

    api_key: str
    api_secret: str
    symbol: str = "BTCUSDT"

    def __post_init__(self):
        self.client = Client(self.api_key, self.api_secret)

    def client(self):
        """Establishes a connection with Binance account, API key values are available at
        Binance developer account"""
        return Client(self.api_key, self.api_secret, {"verify": False, "timeout": 1200})

    def get_order_book(self,
                       limit=50,
                       ):
        """
        Calls the API to collect the order book data for symbol and returns a Dataframe

        :param limit: Number of quotes to be collected in each API call
        :return: A Dataframe including the orderbook information at call moment
        """
        dict_order_book = self.client.get_order_book(symbol=self.symbol,
                                                     limit=limit, requests_params={'timeout': 1200})
        _df = cu.df_list_column_to_multi(tables.create_table(dict_order_book))
        _df.drop(['bids', 'asks', 'lastUpdateId'], axis=1, inplace=True)
        _df_renamed = _df.rename({'bids0': 'bids_price', 'bids1': 'bids_vol',
                                  'asks0': 'asks_price', 'asks1': 'asks_vol'}, axis='columns')
        return _df_renamed

    @ut.run_in_thread
    @tables.continuous_data_collector
    def collect_order_book(self,
                           freq=10,
                           periods=10,
                           limit=50,
                           end_time: datetime = None,
                           add_time=False,
                           csv_name: str = None,  # If given, saves a csv file with this name in memory.
                           ):
        """
        Collects the quotes during a specified period, with the quantity limit determined.
        Either periods or end_time should be determined

        :param freq: The frequency of API call and data collection in seconds
        :param periods: Number of instances that data should be collected for
        :param limit: Number of quotes to be collected in each API call :type int
        :param end_time: The end of collecting period in '%Y-%m-%d %H:%M:%S'
        :param add_time: add a date-time column to the table if set "True"
        :param csv_name: If given, saves a csv file with this name in memory.
        :return: a Dataframe that includes the quotes in the specified interval
        """
        return self.get_order_book(limit=limit)

    def get_trade(self,
                  lookback_window=10,
                  limit=50,
                  ):
        """
        get all the trades in the last interval, with the length specified in lookback_window with,
        limited to the number specified.

        :param lookback_window: The duration of look-back window in seconds
        :param limit: Number of trades for which info should be collected in each call
        :return: A dataframe that includes the details of trades transacted in specified window
        """

        now = datetime.now()
        start_time = (timestamp(now) - lookback_window) * 1000
        end_time = (timestamp(now)) * 1000

        dict_trades = self.client.get_aggregate_trades(
            symbol=self.symbol,
            startTime=start_time,
            endTime=end_time,
            limit=limit,
            requests_params={'timeout': 1200}
        )

        _df = tables.create_table(dict_trades)
        _df.drop(['a', 'f', 'l', 'M'], axis=1, inplace=True)
        _df_renamed = _df.rename({'p': 'price', 'q': 'qty',
                                  'T': 'timestamp', 'm': 'buy'}, axis='columns')

        return _df_renamed

    @ut.run_in_thread
    @tables.continuous_data_collector
    def collect_trades(self,
                       freq=10,
                       periods=10,
                       limit=50,
                       end_time: str = None,
                       add_time=False,
                       csv_name: str = None,
                       ):
        """
        Collects the trades' details during a specified period, with the quantity limit determined.
        Either periods or end_time should be determined

        :param freq: The frequency of API call and data collection in seconds
        :param periods: Number of instances that data should be collected for
        :param limit: Number of trades to be collected in each API call
        :param end_time: The end of collecting period in '%Y-%m-%d %H:%M:%S' format
        :param add_time: add a date-time column to the table if set "True"
        :param csv_name: If given, saves a csv file with this name in memory.
        :return: a Dataframe that includes the trades' information in the specified interval
        """

        return self.get_trade(lookback_window=freq, limit=limit)
