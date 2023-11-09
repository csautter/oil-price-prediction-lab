from abc import ABC, abstractmethod
import pandas as pd


class DataSourcesInterface(ABC):
    """Interface for data sources"""
    @staticmethod
    @abstractmethod
    def get_data(seriesid: str, startyear: str, endyear: str) -> dict:
        """ Get data from the data source

        :param seriesid:
            ID of the series to get data for
        :param startyear:
            Startyear to get data for
        :param endyear:
            Endyear to get data for
        """
        raise NotImplementedError('users must define get_data to use this base class')

    def get_data_as_pandas_df(self, seriesid: str, startyear: str, endyear: str) -> pd.DataFrame:
        """ Get data from the data source as a pandas dataframe

        :param seriesid:
            ID of the series to get data for
        :param startyear:
            Startyear to get data for
        :param endyear:
            Endyear to get data for
        """
        raise NotImplementedError('users must define get_data_as_pandas_df to use this base class')
