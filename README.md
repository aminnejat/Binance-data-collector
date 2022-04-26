# Binance-data-collector
This module utilizes continuous collection and storage of Binance orderbook and trades data, through the API provided by Binance.com

The methods in this module are wrapped by a threading function, thus it gives the user the ability to run desired tests on collected historical data while the data collection job is running. 

To be able to use this module, one needs to get private API-key and API-secret from https://developers.binance.com/.

Below is an example of using `collect_order_book` method, which collects 10 rows of buy/sell quotes information from Binance orderbook, every 10 seconds and for 3 instances, and stores them in a `.csv` file.  


`from Binance import Binance_data as bd`

`example = bd('put your API-key here', 'put your Secret-key here')`

`example.collect_order_book(freq=10, periods=5, limit=10, end_time=None, add_time=True, csv_name='example')`


And the resulting `.csv` file is shown in table below.


|    |   bids_price |   bids_vol |   asks_price |   asks_vol | time                       |
|---:|-------------:|-----------:|-------------:|-----------:|:---------------------------|
|  0 |      40487.9 |    3.47675 |      40487.9 |    3.50426 | 2022-04-25 19:37:19.773342 |
|  1 |      40487.5 |    0.00254 |      40488   |    0.6     | 2022-04-25 19:37:19.773342 |
|  2 |      40486.6 |    0.0493  |      40488.8 |    0.02141 | 2022-04-25 19:37:19.773342 |
|  3 |      40486.5 |    0.00579 |      40489.1 |    0.05043 | 2022-04-25 19:37:19.773342 |
|  4 |      40485.7 |    0.01053 |      40489.5 |    0.8     | 2022-04-25 19:37:19.773342 |
|  5 |      40485.3 |    0.0784  |      40490   |    0.02461 | 2022-04-25 19:37:19.773342 |
|  6 |      40485.1 |    0.33343 |      40490.2 |    0.00519 | 2022-04-25 19:37:19.773342 |
|  7 |      40484.5 |    0.005   |      40490.2 |    0.06    | 2022-04-25 19:37:19.773342 |
|  8 |      40484.5 |    0.12375 |      40490.5 |    0.07264 | 2022-04-25 19:37:19.773342 |
|  9 |      40484.4 |    0.04883 |      40490.5 |    0.24853 | 2022-04-25 19:37:19.773342 |
| 10 |      40480   |    3.05063 |      40480   |    5.71727 | 2022-04-25 19:37:29.909643 |
| 11 |      40480   |    0.00488 |      40480.2 |    0.01294 | 2022-04-25 19:37:29.909643 |
| 12 |      40479.8 |    0.0004  |      40481.2 |    0.8     | 2022-04-25 19:37:29.909643 |
| 13 |      40479.7 |    0.00236 |      40481.5 |    0.85043 | 2022-04-25 19:37:29.909643 |
| 14 |      40479.6 |    0.0011  |      40482.1 |    0.07434 | 2022-04-25 19:37:29.909643 |
| 15 |      40479.5 |    0.001   |      40482.1 |    0.05043 | 2022-04-25 19:37:29.909643 |
| 16 |      40479.4 |    0.0011  |      40482.6 |    0.12351 | 2022-04-25 19:37:29.909643 |
| 17 |      40479.3 |    0.002   |      40482.8 |    0.00026 | 2022-04-25 19:37:29.909643 |
| 18 |      40479.2 |    0.0024  |      40483.6 |    0.10119 | 2022-04-25 19:37:29.909643 |
| 19 |      40479   |    0.00252 |      40483.6 |    0.3335  | 2022-04-25 19:37:29.909643 |
| 20 |      40480.6 |    6.68902 |      40480.6 |    0.42385 | 2022-04-25 19:37:40.036549 |
| 21 |      40480.2 |    0.26028 |      40480.6 |    0.00918 | 2022-04-25 19:37:40.036549 |
| 22 |      40480   |    0.0011  |      40480.6 |    0.61911 | 2022-04-25 19:37:40.036549 |
| 23 |      40480   |    0.0792  |      40481.9 |    0.00138 | 2022-04-25 19:37:40.036549 |
| 24 |      40479.8 |    0.0004  |      40482.1 |    0.07434 | 2022-04-25 19:37:40.036549 |
| 25 |      40479.8 |    0.00251 |      40482.8 |    0.00026 | 2022-04-25 19:37:40.036549 |
| 26 |      40479.6 |    0.0011  |      40483.7 |    0.20003 | 2022-04-25 19:37:40.036549 |
| 27 |      40479.5 |    0.001   |      40483.7 |    0.8     | 2022-04-25 19:37:40.036549 |
| 28 |      40479.4 |    0.12349 |      40483.7 |    0.33349 | 2022-04-25 19:37:40.036549 |
| 29 |      40479.4 |    0.0011  |      40484.7 |    0.41931 | 2022-04-25 19:37:40.036549 |
