import os
import sys
from typing import Literal

import requests
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from .AlphaVantageCache import AlphaVantageCache

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_source_interfaces.DataSourcesInterface import DataSourcesInterface


class AlphaVantageCommodities(DataSourcesInterface):
    @staticmethod
    def get_cache_directory() -> str:
        return AlphaVantageCache.get_cache_directory()

    def __request_url_builder(self, function: str = None, interval: str = None) -> str:
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
        r = requests.get(self.__request_url_builder(function=seriesid, interval=interval))
        data = r.json()
        return data

    def get_data_as_pandas_df(self, seriesid: str, startyear: str = None, endyear: str = None) -> pd.DataFrame:
        df = pd.DataFrame(self.get_data(seriesid)['data'])
        return df
