from ...config import FBPROPHET_PERIODS, FBPROPHET_FREQ, FBPROPHET_HYPERPARAMS_PATH, FBPROPHET_MODELS_PATH
from ...fbprophet.utils import load_model, save_model
from fbprophet import Prophet
from typing import Optional
import json
import pandas as pd


def predict(plant_data_id: str,
            measurement: str,
            periods: int = FBPROPHET_PERIODS,
            freq: int = FBPROPHET_FREQ,
            models_path: str = FBPROPHET_MODELS_PATH,
            ) -> pd.DataFrame:
    m = load_model(plant_data_id, measurement, models_path)
    if not m:
        raise FileNotFoundError
    future = m.make_future_dataframe(periods=periods, freq=f'{freq}S')
    return m.predict(future)


def fit_and_predict(plant_data_id: str,
                    data: pd.DataFrame,
                    measurement: str,
                    periods: int = FBPROPHET_PERIODS,
                    freq: int = FBPROPHET_FREQ,
                    hyperparams: Optional[dict] = None,
                    hyperparams_path: str = FBPROPHET_HYPERPARAMS_PATH,
                    models_path: str = FBPROPHET_MODELS_PATH,
                    ) -> pd.DataFrame:
    if hyperparams:
        params = hyperparams
    else:
        df = pd.read_csv(hyperparams_path)
        row_index = (df['plant_data_id'] == plant_data_id) & (df['measurement'] == measurement)
        params_string = df.loc[row_index, 'hyperparams'].iloc[0]
        params = json.loads(params_string)

    m = Prophet(**params)
    m.fit(data)
    save_model(plant_data_id, measurement, m, models_path)
    future = m.make_future_dataframe(periods=periods, freq=f'{freq}S')
    return m.predict(future)


def prepare_prophet_df(source_df: pd.DataFrame, y_col_name: str, ds_col_name: str = 'creation_date') -> pd.DataFrame:
    """
    Returns a Dataframe with two columns 'ds' and 'y' usable by Prophet
    :param source_df: Dataframe containing data
    :param y_col_name: Name of the column of the source Dataframe to be mapped into the target 'y' column
    :param ds_col_name: Name of the column of the source Dataframe to be mapped into the target 'ds' column
    :return: Returns a Dataframe with two columns 'ds' and 'y' usable by Prophet
    """
    new_df = source_df[[ds_col_name, y_col_name]].copy()
    return new_df.rename(columns={ds_col_name: 'ds', y_col_name: 'y'})


def filter_time_window(df: pd.DataFrame, start_date=None, end_date=None, ds_col_name: str = 'ds') -> pd.DataFrame:
    """
    Filters a Dataframe containing a datetime column by [start_date, end_date)
    :param df: Source dataframe to filter
    :param start_date: Starting point of filtering. Inclusive.
    :param end_date: Optional ending point of filtering. Exclusive.
    :param ds_col_name: Name of the column that contains datetime data to filter
    :return:
    """
    df2 = df
    if start_date:
        df2 = df2.loc[df[ds_col_name] >= start_date]
    if end_date:
        df2 = df2.loc[df2[ds_col_name] < end_date]
    return df2


def find_start_date(df: pd.DataFrame, time_window: str):
    if time_window == 'last_week':
        start_date = df['creation_date'].iloc[-1] + pd.DateOffset(-7)
    elif time_window == 'last_month':
        start_date = df['creation_date'].iloc[-1] + pd.DateOffset(-30)
    else:
        start_date = df['creation_date'].iloc[0]
    return start_date
