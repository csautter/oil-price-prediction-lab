import os
import sys
from abc import ABC, abstractmethod
import pandas as pd


class DataSourcesInterface(ABC):
    """Interface for data sources"""

    @abstractmethod
    def get_cache_directory(self) -> str:
        raise NotImplementedError('create property cache_directory')

    @abstractmethod
    def get_data(self, seriesid: str, startyear: str = None, endyear: str = None) -> dict:
        raise NotImplementedError('users must define get_data to use this base class')

    @abstractmethod
    def get_data_as_pandas_df(self, seriesid: str, startyear: str = None, endyear: str = None) -> pd.DataFrame:
        raise NotImplementedError('users must define get_data_as_pandas_df to use this base class')
