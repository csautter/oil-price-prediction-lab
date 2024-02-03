import pandas as pd
import numpy as np


class PandasDataFrameNormalizer:
    """Normalizes single columns of a pandas dataframe"""
    __max: float = None
    __min: float = None

    def normalize_pandas_data_frame_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Normalizes a pandas dataframe"""
        if self.__max is None:
            self.__max = df[column].max()
        if self.__min is None:
            self.__min = df[column].min()

        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        df.sort_values(by=['date'], inplace=True)
        return df

    def inverse_transform_single_value(self, value: float) -> float:
        """Inverse transform single value"""
        return value * (self.__max - self.__min) + self.__min

    def inverse_transform_pandas_data_frame_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Inverse transform pandas data frame column"""
        df[column] = self.inverse_transform_single_value(df[column])
        df.sort_values(by=['date'], inplace=True)
        return df

    def inverse_transform_numpy_array(self, array: np.array) -> np.array:
        """Inverse transform numpy array"""
        return array * (self.__max - self.__min) + self.__min

    def inverse_transform_numpy_array_column(self, array: np.array, column: int) -> np.array:
        """Inverse transform numpy array column"""
        return array[:, column] * (self.__max - self.__min) + self.__min

    def inverse_transform_list(self, input_list: list) -> list:
        """Inverse transform list"""
        return [self.inverse_transform_single_value(x) for x in input_list]
