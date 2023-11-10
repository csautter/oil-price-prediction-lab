import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bls_gov.BlsGov import BlsGov


# import data_sources.us_bureau_of_labor_statistics.BlsGov as BlsGov
# from .. import BlsGov

class TestBlsGov(unittest.TestCase):
    def test_get_data(self):
        bls = BlsGov()
        data = bls.get_data('LNU02000000', '2010', '2019')
        self.assertTrue(len(data) > 0)
        self.assertEqual('REQUEST_SUCCEEDED', data['status'])

    def test_get_data_out_of_range(self):
        bls = BlsGov()
        with self.assertRaises(Exception):
            bls.get_data('LNU02000000', '2000', '2021')

    def test_check_date_range(self):
        bls = BlsGov()
        with self.assertRaises(Exception):
            bls.check_date_range('2000', '2021')
        self.assertTrue(bls.check_date_range('2000', '2019'))
