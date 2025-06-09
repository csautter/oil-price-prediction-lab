import os
import urllib.request
import pandas as pd
from .BlsCache import BlsCache

from dotenv import load_dotenv

load_dotenv()


class BlsGovGetSeriesDescription:
    series_id: str = None
    database_id: str = None
    local_filename: str = None

    def __init__(self, series_id: str) -> None:
        self.series_id = series_id
        self.__extract_database_id()
        self.__generate_local_filename()

    def __extract_database_id(self) -> None:
        self.database_id = self.series_id[0:2]

    def __generate_local_filename(self) -> None:
        self.local_filename = BlsCache.get_cache_directory() + '/' + self.database_id.lower() + '.series'

    def __download_series_description(self) -> None:
        remote_url = 'https://download.bls.gov/pub/time.series/' + self.database_id.lower() + '/' + self.database_id.lower() + '.series'
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', os.environ['BLS_GOV_USER_AGENT'])]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(remote_url, self.local_filename)

    def get_series_description(self) -> pd.DataFrame:
        # if local file exists, read from local file
        if not os.path.isfile(self.local_filename):
            self.__download_series_description()

        with open(self.local_filename) as csv_file:
            df = pd.read_csv(csv_file, sep='\t', low_memory=False)

        # remove leading and trailing whitespaces from column names
        df.columns = df.columns.str.strip()

        # remove leading and trailing whitespaces from values in column 'series_id'
        df['series_id'] = df['series_id'].apply(lambda x: x.strip())

        df_row = df.loc[df['series_id'] == self.series_id]

        return df_row

    def get_series_id(self) -> str:
        df_row = self.get_series_description()
        return df_row['series_id'].values[0]

    def get_area_code(self) -> str:
        df_row = self.get_series_description()
        return df_row['area_code'].values[0]

    def get_item_code(self) -> str:
        df_row = self.get_series_description()
        return df_row['item_code'].values[0]

    def get_seasonal(self) -> str:
        df_row = self.get_series_description()
        return df_row['seasonal'].values[0]

    def get_periodicity_code(self) -> str:
        df_row = self.get_series_description()
        return df_row['periodicity_code'].values[0]

    def get_base_code(self) -> str:
        df_row = self.get_series_description()
        return df_row['base_code'].values[0]

    def get_base_period(self) -> str:
        df_row = self.get_series_description()
        return df_row['base_period'].values[0]

    def get_series_title(self) -> str:
        df_row = self.get_series_description()
        return df_row['series_title'].values[0]

    def get_footnote_codes(self) -> list:
        df_row = self.get_series_description()
        return df_row['footnote_codes'].values[0].split(',')

    def get_begin_year(self) -> int:
        df_row = self.get_series_description()
        return df_row['begin_year'].values[0]

    def get_begin_period(self) -> int:
        df_row = self.get_series_description()
        return df_row['begin_period'].values[0]

    def get_end_year(self) -> int:
        df_row = self.get_series_description()
        return df_row['end_year'].values[0]

    def get_end_period(self) -> int:
        df_row = self.get_series_description()
        return df_row['end_period'].values[0]

    def get_link_to_timeseries_viewer(self) -> str:
        link = 'https://beta.bls.gov/dataViewer/view/timeseries/' + self.series_id
        return link
