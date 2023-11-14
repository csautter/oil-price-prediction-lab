from abc import ABC, abstractmethod
import pandas as pd


class DataSourcesInterface(ABC):
    """Interface for data sources"""

    @abstractmethod
    def get_data(self, seriesid: str, startyear: str = None, endyear: str = None) -> dict:
        raise NotImplementedError('users must define get_data to use this base class')

    @abstractmethod
    def get_data_as_pandas_df(self, seriesid: str, startyear: str = None, endyear: str = None) -> pd.DataFrame:
        raise NotImplementedError('users must define get_data_as_pandas_df to use this base class')

    @staticmethod
    @abstractmethod
    def get_all_curated_series_ids() -> list:
        """Returns a list of all curated series ids"""
        raise NotImplementedError('users must define get_all_curated_series_ids to use this base class')

    @staticmethod
    @abstractmethod
    def plot_series_id(self, seriesid: str, startyear: str = None, endyear: str = None):
        """Plots the series id"""
        raise NotImplementedError('users must define plot_series_id to use this base class')