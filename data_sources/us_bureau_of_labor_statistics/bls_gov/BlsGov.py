import requests
import json
import os
import sys
import pandas as pd
from matplotlib import pyplot as plt
from .BlsCache import BlsCache
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_source_interfaces.DataSourcesInterface import DataSourcesInterface


class BlsGov(DataSourcesInterface):
    @staticmethod
    def get_cache_directory() -> str:
        return BlsCache.get_cache_directory()

    @staticmethod
    def check_date_range(startyear: str, endyear: str) -> bool:
        year_diff = int(endyear) - int(startyear)
        if year_diff > 20:
            raise Exception('Registered users may request up to 20 years per query.')
        else:
            return True

    def get_data(self, seriesid: str, startyear: str, endyear: str) -> dict:
        BlsGov.check_date_range(startyear, endyear)
        filename = self.get_cache_directory() + '/' + seriesid + '/startyear' + startyear + '_endyear' + endyear + '.json'
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
        df = self.convert_json_to_pandas_df(json_data)

        if seriesid.startswith('LN'):
            df['value'] = pd.to_numeric(df['value'])
            df['day'] = 1
            df['merged'] = df['year'] + '-' + df['periodName'] + '-' + df['day'].astype(str)
            df['date'] = pd.to_datetime(df['merged'], format='%Y-%B-%d')
            df.drop(['year', 'periodName', 'day', 'merged', 'period'], axis=1, inplace=True)
            df.sort_values(by=['date'], inplace=True)

        return df

    @staticmethod
    def get_all_curated_series_ids() -> list:
        return [
            'LNU02000000',  # (Unadj) Employment Level
            'LNU01000000',  # (Unadj) Civilian Labor Force Level
            'LNU03000000',  # (Unadj) Unemployment Level
            'CIU1010000000000I',  # Total compensation for All Civilian workers in All industries and occupations, Index
            'CIU2020000000000I',
            # Wages and salaries for Private industry workers in All industries and occupations, Index

            'EIUIQ',  # Monthly export price index for BEA End Use, All commodities, not seasonally adjusted
            'EIUIR',  # Monthly import price index for BEA End Use, All commodities, not seasonally adjusted
            'APU000072511',
            # Fuel oil #2 per gallon (3.785 liters) in U.S. city average, average price, not seasonally adjusted

            'PCU212---212---',  # PPI industry sub-sector data for Mining (except oil & gas), not seasonally adjusted
            'PCU211---211---',  # PPI industry sub-sector data for Oil and gas extraction, not seasonally adjusted
            'PCU2111--2111--',  # PPI industry group data for Oil and gas extraction, not seasonally adjusted
            'PCU2111--2111--',  # PPI industry group data for Oil and gas extraction, not seasonally adjusted
            'PCU333914333914113',
            # PPI industry data for Measuring, dispensing, and other pumping equipment mfg-Oil-well and oil-field
            # pumps, except boiler feed, not seasonally adjusted

            'PCU21311121311105',
            # PPI industry data for Drilling oil and gas wells-Reworking oil and gas wells, not seasonally adjusted

            'WPU114119153',
            # PPI Commodity data for Machinery and equipment-Oil-well and oil-field pumps, not seasonally adjusted

            'PCU333132333132',
            # PPI industry data for Oil and gas field machinery and equipment mfg, not seasonally adjusted

            'WPUFD49207',  # PPI Commodity data for Final demand-Finished goods, not seasonally adjusted
            'WPUFD49116',
            # PPI Commodity data for Final demand less foods, energy, and trade services, not seasonally adjusted

            'WPUFD49104',  # PPI Commodity data for Final demand less foods and energy, not seasonally adjusted
            'WPUFD4',  # PPI Commodity data for Final demand, not seasonally adjusted
            'CUUR0000SA0',  # All items in U.S. city average, all urban consumers, not seasonally adjusted
        ]

    def plot_series_id(self, seriesid: str,
                       startyear: str = None,
                       endyear: str = None) -> pd.DataFrame:
        df = self.get_data_as_pandas_df(seriesid, startyear, endyear)

        df.plot(x="date", y='value', linewidth=1)
        plt.xlabel("Date", size=10)
        plt.ylabel("Price", size=10)
        plt.show()

        return df
