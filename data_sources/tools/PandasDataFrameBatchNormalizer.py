import numpy as np
import pandas as pd
from PandasDataFrameNormalizer import PandasDataFrameNormalizer


class PandasDataFrameBatchNormalizer:
    """Normalizes a pandas dataframe"""

    __normalizer: dict[str, PandasDataFrameNormalizer] = {}
    __ignore_columns: list = []

    def normalize_pandas_data_frame(self, df: pd.DataFrame, ignore_columns: list) -> pd.DataFrame:
        """Normalizes a pandas dataframe"""

        self.__ignore_columns = ignore_columns

        for column in df.columns:
            if column in self.__ignore_columns:
                continue

            if column not in self.__normalizer:
                print('create new normalizer for column: ' + column)
                self.__normalizer[column] = PandasDataFrameNormalizer()

            print('normalize column: ' + column)
            df = self.__normalizer[column].normalize_pandas_data_frame_column(df, column)

        df.sort_values(by=['date'], inplace=True)
        return df

    def inverse_transform_pandas_data_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """Inverse transform pandas data frame"""

        for column in df.columns:
            if column not in self.__normalizer:
                self.__normalizer[column] = PandasDataFrameNormalizer()

            df[column] = self.__normalizer[column].inverse_transform_pandas_data_frame_column(df, column)

        df.sort_values(by=['date'], inplace=True)
        return df

    def inverse_transform_numpy_array(self, array: np.array, column: str) -> np.array:
        """Inverse transform numpy array"""

        return self.__normalizer[column].inverse_transform_numpy_array(array)