from abc import ABC, abstractmethod


class DataSourcesInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_data(self, seriesid, startyear, endyear):
        raise NotImplementedError('users must define get_data to use this base class')

    def get_data_as_pandas_df(self, seriesid, startyear, endyear):
        raise NotImplementedError('users must define get_data_as_pandas_df to use this base class')
