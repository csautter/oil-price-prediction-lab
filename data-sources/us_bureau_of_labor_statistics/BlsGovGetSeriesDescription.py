import os
import urllib.request
import pandas as pd

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
        self.local_filename = 'cache/' + self.database_id.lower() + '.series'

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
