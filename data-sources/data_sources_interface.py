import abc

class DataSourcesInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_data(self, seriesid, startyear, endyear):
        pass
