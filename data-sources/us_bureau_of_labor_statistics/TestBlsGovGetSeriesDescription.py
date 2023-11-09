import unittest
from BlsGovGetSeriesDescription import BlsGovGetSeriesDescription


class TestBlsGovGetSeriesDescription(unittest.TestCase):
    def test_get_series_description(self):
        bls = BlsGovGetSeriesDescription('CUSR0000SA0')
        data = bls.get_series_description()
        print(data)
        self.assertTrue(len(data) > 0)
        self.assertEqual('CUSR0000SA0', data['series_id'].values[0])

    def test_get_series_description_with_invalid_series_id(self):
        bls = BlsGovGetSeriesDescription('LNU02000001')
        data = bls.get_series_description()
        self.assertTrue(len(data) == 0)