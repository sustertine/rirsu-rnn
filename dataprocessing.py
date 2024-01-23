import pickle

import pandas as pd
from sklearn.preprocessing import PowerTransformer, MinMaxScaler, StandardScaler

class DataProcessor:
    def __init__(self):
        with open('objects/mms-scaler.pkl', 'rb') as file:
            self.mms = pickle.load(file)
        with open('objects/std-scaler.pkl', 'rb') as file:
            self.std = pickle.load(file)

    def _check_columns(self, df):
        requiredColumns = {'NO2', 'PM2.5', 'O3', 'PM10', 'temperature_2m (°C)', 'relative_humidity_2m (%)',
                            'dew_point_2m (°C)', 'apparent_temperature (°C)', 'precipitation (mm)',
                            'pressure_msl (hPa)', 'surface_pressure (hPa)'}
        if not requiredColumns.issubset(df.columns):
            raise ValueError("Missing columns in DataFrame")
        return df

    def _check_nan(self, df):
        if df.isna().any().any():
            raise ValueError("NaN values present in DataFrame")
        return df

    def _check_datetime_index(self, df):
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame index is not a datetime index")
        if not df.index.is_monotonic_increasing:
            df = df.sort_index()
        return df

    def _apply_power_transform(self, df):
        pt = PowerTransformer(method='yeo-johnson')
        for column in df.select_dtypes(include=['float64', 'int64']).columns:
            df[column] = pt.fit_transform(df[[column]])
        return df

    def _apply_scaling(self, df):
        minmaxcols = ['PM2.5', 'O3', 'relative_humidity_2m (%)', 'dew_point_2m (°C)',
                        'apparent_temperature (°C)', 'precipitation (mm)']
        stdcols = ['NO2', 'PM10', 'temperature_2m (°C)', 'pressure_msl (hPa)', 'surface_pressure (hPa)']

        df[minmaxcols] = self.mms.fit_transform(df[minmaxcols])
        df[stdcols] = self.std.fit_transform(df[stdcols])
        return df

    def _create_features(self, df):
        df['lag1_NO2'] = df['NO2'].shift(1)
        df['roll_mean_PM10_7d'] = df['PM10'].rolling(window=7).mean()
        df['diff_PM2.5'] = df['PM2.5'].diff()
        threshold_NO2 = df['NO2'].quantile(0.75)
        df['cum_count_high_NO2'] = (df['NO2'] > threshold_NO2).cumsum()
        df['NO2_O3_interaction'] = df['NO2'] * df['O3']
        df['PM2.5_squared'] = df['PM2.5'] ** 2
        # df['O3_quartile'] = pd.qcut(df['O3'], q=4, labels=False)
        df['roll_var_PM2.5_7d'] = df['PM2.5'].rolling(window=7).var()
        df['diff_PM10'] = df['PM10'].diff()
        df = df.fillna(method='bfill')
        df = df.drop('PM10', axis=1)
        return df[['diff_PM10', 'PM2.5_squared', 'PM2.5', 'roll_mean_PM10_7d',
                                           'cum_count_high_NO2', 'dew_point_2m (°C)', 'diff_PM2.5',
                                           'roll_var_PM2.5_7d']]

    def _create_sliding_windows(self, df, window_size, step_size=1):
        windows = []
        for start in range(0, len(df) - window_size + 1, step_size):
            end = start + window_size
            window = df.iloc[start:end]
            windows.append(window)
        return windows

    def processDf(self, df):
        df = self._check_columns(df)
        df = self._check_nan(df)
        df = self._check_datetime_index(df)
        df = self._apply_power_transform(df)
        df = self._apply_scaling(df)
        df = self._create_features(df)
        windows = self._create_sliding_windows(df, 21)

        return windows

    def reverse_scaling(self, column):
        column_reshaped = column.values.reshape(-1, 1)
        reversed_scaled_column = self.std.inverse_transform(column_reshaped)

        return pd.Series(reversed_scaled_column.flatten(), index=column.index)
