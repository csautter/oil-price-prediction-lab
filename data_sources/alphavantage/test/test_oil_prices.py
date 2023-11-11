import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alphavantage_api.AlphaVantageCommodities import AlphaVantageCommodities


class TestAlphaVantageCommodities(unittest.TestCase):
    def test_get_data(self):
        av = AlphaVantageCommodities()
        data = av.get_data('WTI')
        print(data)

    def test_get_data_as_pandas_df(self):
        av = AlphaVantageCommodities()
        df = av.get_data_as_pandas_df('WTI')
        print(df)
