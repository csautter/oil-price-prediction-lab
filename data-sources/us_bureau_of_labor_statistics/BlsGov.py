import requests
import json
import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, "..")

from data_sources_interface import DataSourcesInterface


class BlsGov(DataSourcesInterface):
    @staticmethod
    def check_date_range(startyear: str, endyear: str) -> bool:
        year_diff = int(endyear) - int(startyear)
        if year_diff > 20:
            raise Exception('Registered users may request up to 20 years per query.')
        else:
            return True

    @staticmethod
    def get_data(seriesid: str, startyear: str, endyear: str) -> dict:
        BlsGov.check_date_range(startyear, endyear)
        filename = 'cache/' + seriesid + '/startyear' + startyear + '_endyear' + endyear + '.json'
        if os.path.isfile(filename):
            with open(filename) as json_file:
                json_data = json.load(json_file)
                return json_data

        headers = {'Content-type': 'application/json'}
        data = json.dumps(
            {
                "seriesid": [seriesid],
                "startyear": startyear,
                "endyear": endyear,
                "registrationkey": os.environ['API_TOKEN_US_BUREAU_OF_LABOR_STATISTICS']
            }
        )
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)

        print(json_data['message'])
        if len(json_data['message']) > 0:
            raise Exception(json_data['message'][0])

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(json.dumps(json_data))

        return json_data

    @staticmethod
    def convert_json_to_pandas_df(json_data: object) -> pd.DataFrame:
        json_timeseries = json_data['Results']['series'][0]['data']
        df = pd.DataFrame(json_timeseries)
        return df

    def get_data_as_pandas_df(self, seriesid: str, startyear: str, endyear: str):
        json_data = self.get_data(seriesid, startyear, endyear)
        return self.convert_json_to_pandas_df(json_data)
