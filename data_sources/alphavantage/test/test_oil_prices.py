import unittest
import os
import sys
import numpy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alphavantage_api.AlphaVantageCommodities import AlphaVantageCommodities


class TestAlphaVantageCommodities(unittest.TestCase):
    def test_get_data(self):
        av = AlphaVantageCommodities()
        data = av.get_data('WTI')
        self.assertTrue(data['data'][0]) # check if data is not empty

    def test_get_data_as_pandas_df(self):
        av = AlphaVantageCommodities()
        df = av.get_data_as_pandas_df('WTI')
        print("Value of df['value'][0]: " + str(df['value'][0]))
        print("Type of df['value'][0]: ")
        t = type(df['value'][0])
        print(t)
        self.assertTrue(df['value'][0] > 0)
        self.assertTrue(t == numpy.float32)
