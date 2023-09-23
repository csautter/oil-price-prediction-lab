import abc

class DataSourcesInterface(abc.ABC):
    @abc.abstractmethod
    def get_data(self, seriesid, startyear, endyear):
        pass