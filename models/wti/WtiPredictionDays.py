from pathlib import Path
import os
import sys
from typing import Literal

sys.path.insert(0, os.path.abspath(os.path.join(Path().resolve(), '../..')))
from ImportHelper import ImportHelper

ImportHelper()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import *
# from tensorflow import keras
from sklearn import preprocessing
from AlphaVantageCommodities import AlphaVantageCommodities
from PandasDataFrameBatchNormalizer import PandasDataFrameBatchNormalizer
from dotenv import load_dotenv
import seaborn as sns
import datetime

load_dotenv()


class WtiPredictionDays:
    """
    This class is used to predict the WTI price for the next days.
    """
    verbose: bool = False
    date_range_limits: dict = {'start': None, 'end': None}
    nan_handling: Literal['drop', 'fill', 'keep', 'generate_average'] = 'keep'
    output_column: str = 'WTI_value'
    feature_columns: list = ['WTI_value', 'BRENT_value', 'NATURAL_GAS_value']
    pd_batch_normalizer: PandasDataFrameBatchNormalizer = PandasDataFrameBatchNormalizer()
    training_data_size: float = 0.8
    forecast_days: int = 1
    epochs: int = 100
    features_sequence_length: int = 60
    sampling_rate: int = 1
    batch_size: int = 32

    def __init__(self, verbose: bool = False) -> None:
        """
        Constructor.
        :param verbose: controls the verbosity of the class
        """
        self.verbose: bool = verbose

    def create_data_collection(self) -> pd.DataFrame:
        """
        Create the data collection.
        :return: pd.DataFrame with the data collection
        """
        avc = AlphaVantageCommodities()
        avc_selected_symbols = ['WTI', 'BRENT', 'NATURAL_GAS']

        if self.verbose:
            print('avc_selected_symbols: ' + str(avc_selected_symbols))
            print('print data for each symbol')
            for symbol in avc_selected_symbols:
                avc.plot_series_id(symbol)

        df_merged = avc.get_data_as_pandas_df_multiple_series_ids(avc_selected_symbols)
        return df_merged

    def set_date_range_limits(self, start: str = None, end: str = None) -> None:
        """
        Set the date range limits for the data collection.
        :param start: start date in format YYYY-MM-DD
        :param end: end date in format YYYY-MM-DD
        :return: None
        """
        try:
            if start is not None:
                datetime.datetime.strptime(start, '%Y-%m-%d')
                self.date_range_limits['start'] = start
            if end is not None:
                datetime.datetime.strptime(end, '%Y-%m-%d')
                self.date_range_limits['end'] = end
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def get_date_range_limits(self) -> dict:
        """
        Get the date range limits for the data collection.
        :return: dict with keys 'start' and 'end'
        """
        return self.date_range_limits

    def set_nan_handling(self, nan_handling: Literal['drop', 'fill', 'keep', 'generate_average']) -> None:
        """
        Set the nan handling for the data collection.
        :param nan_handling: nan handling
        :return: None
        """
        self.nan_handling = nan_handling

    def data_collection_normalization(self, df: pd.DataFrame, ignore_columns: list) -> pd.DataFrame:
        """
        Normalize the data collection.
        :param ignore_columns: columns to ignore during normalization
        :param df: pd.DataFrame with the data collection
        :return: pd.DataFrame with the normalized data collection
        """
        if self.verbose:
            print('show df.head() before normalization: ')
            print(df.head())

        df = self.pd_batch_normalizer.normalize_pandas_data_frame(df, ignore_columns)

        if self.nan_handling == 'drop':
            df = df.dropna()
        elif self.nan_handling == 'fill':
            df = df.dropna(subset=[self.output_column]).fillna(-1)
        elif self.nan_handling == 'generate_average':
            raise NotImplementedError('nan_handling == generate_average is not implemented yet')

        if self.verbose:
            print('show df.head() after normalization: ')
            print(df.head())

        return df

    def inverse_transform_numpy_array(self, array: np.array) -> np.array:
        """Inverse transform numpy array"""
        return self.pd_batch_normalizer.inverse_transform_numpy_array(array, self.output_column)

    def data_collection_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data collection.
        :param df: pd.DataFrame with the data collection
        :return: pd.DataFrame with the preprocessed data collection
        """
        if self.verbose:
            print('show df.head() before preprocessing: ')
            print(df.head())

        if self.date_range_limits['start'] is not None:
            df = df[df['date'].ge(self.date_range_limits['start'])]

        if self.date_range_limits['end'] is not None:
            df = df[df['date'].le(self.date_range_limits['end'])]

        df = df.reset_index(drop=True)

        if self.verbose:
            print('show df.head() after preprocessing: ')
            print(df.head())

        return df

    def split_data_collection_into_numpy_arrays(self, df: pd.DataFrame) -> tuple:
        """
        Split the data collection into numpy arrays.
        :param df: pd.DataFrame with the data collection
        :return: tuple with numpy arrays - x_train, y_train, x_test, y_test
        """
        data = df[self.feature_columns].to_numpy()
        split_at = int(len(data) * self.training_data_size)

        train = data[0:split_at]
        x_train = train[:-(self.features_sequence_length + self.forecast_days)]
        y_train = train[self.features_sequence_length + self.forecast_days:, 0]

        test = data[split_at+1:]
        x_test = test[:-(self.features_sequence_length + self.forecast_days)]
        y_test = test[self.features_sequence_length + self.forecast_days:, 0]

        return x_train, y_train, x_test, y_test
