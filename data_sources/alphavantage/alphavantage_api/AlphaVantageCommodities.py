import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Literal
import matplotlib.pyplot as plt
import requests
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(Path().resolve(), '../../..')))
from ImportHelper import ImportHelper
ImportHelper()

from AlphaVantageCache import AlphaVantageCache
from DataSourcesInterface import DataSourcesInterface


class AlphaVantageCommodities(DataSourcesInterface):
    @staticmethod
    def __request_url_builder(function: str = None, interval: str = None) -> str:
        parts: list = []

        if function is not None:
            parts.append('function=' + function)

        if interval is not None:
            parts.append('interval=' + interval)

        url = 'https://www.alphavantage.co/query?'+'&'.join(parts)+'&apikey=' + os.environ['ALPHA_VANTAGE_API_KEY']
        return url

    def get_data(self, seriesid: str,
                 startyear: str = None,
                 endyear: str = None,
                 interval: Literal['daily', 'weekly', 'monthly'] = 'daily') -> dict:

        today = date.today()
        filename = AlphaVantageCache.get_cache_directory() + '/' + str(today) + '_' + seriesid + '_'+interval+'.json'

        # read data from cache if exists
        if os.path.isfile(filename):
            with open(filename) as json_file:
                json_data = json.load(json_file)
                return json_data

        # request data from API
        r = requests.get(self.__request_url_builder(function=seriesid, interval=interval))
        json_data = r.json()

        # write data to cache
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(json.dumps(json_data))

        return json_data

    def get_data_as_pandas_df(self, seriesid: str,
                              startyear: str = None,
                              endyear: str = None,
                              interval: Literal['daily', 'weekly', 'monthly'] = 'daily') -> pd.DataFrame:

        df = pd.DataFrame(self.get_data(seriesid, startyear, endyear, interval)['data'])
        df = df[df['value'] != '.']
        df[seriesid+'_value'] = pd.to_numeric(df['value'], downcast="float")
        df.drop(['value'], axis=1, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values(by=['date'], inplace=True)
        return df

    @staticmethod
    def get_all_curated_series_ids() -> list:
        curated_series_ids = [
            'WTI',
            'BRENT',
            'NATURAL_GAS'
        ]
        return curated_series_ids

    def plot_series_id(self, seriesid: str,
                       startyear: str = None,
                       endyear: str = None,
                       interval: Literal['daily', 'weekly', 'monthly'] = 'daily') -> pd.DataFrame:
        df = self.get_data_as_pandas_df(seriesid, startyear, endyear, interval)
        df.plot(x="date", y=seriesid+'_value', linewidth=1)
        plt.xlabel("Date", size=10)
        plt.ylabel("Price", size=10)
        plt.title(seriesid + " Price", size=15)
        plt.show()

        return df

    def plot_multiple_series_ids(self, seriesids: list,
                                 startyear: str = None,
                                 endyear: str = None,
                                 interval: Literal['daily', 'weekly', 'monthly'] = 'daily') -> None:
        for seriesid in seriesids:
            self.plot_series_id(seriesid, startyear, endyear, interval)

    def get_data_as_pandas_df_multiple_series_ids(self, seriesids: list,
                                                  startyear: str = None,
                                                  endyear: str = None,
                                                  interval: Literal['daily', 'weekly', 'monthly'] = 'daily') -> pd.DataFrame:
        df = self.get_data_as_pandas_df(seriesids.pop(0), startyear, endyear, interval)
        for seriesid in seriesids:
            df = df.merge(self.get_data_as_pandas_df(seriesid, startyear, endyear, interval), on='date', how='outer')

        return df