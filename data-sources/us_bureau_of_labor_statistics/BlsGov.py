import pandas as pd
import requests
import json
import os
import sys
sys.path.insert(0,"..")
from data_sources_interface import DataSourcesInterface

class BlsGov(DataSourcesInterface):
    @staticmethod
    def check_date_range(startyear, endyear):
        year_diff = int(endyear) - int(startyear)
        if year_diff > 20:
            raise Exception('Registered users may request up to 20 years per query.')

    def get_data(self, seriesid, startyear, endyear):
        super.get_data(seriesid, startyear, endyear)
        BlsGov.check_date_range(startyear, endyear)
        filename = 'cache/'+seriesid+'/startyear'+startyear+'_endyear'+endyear+'.json'
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

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(json.dumps(json_data))

        return json_data