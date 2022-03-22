from ..models import PlantDataModel, db
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
import itertools
import pandas as pd


def create_param_combinations(**param_dict):
    param_iter = itertools.product(*param_dict.values())
    params = []
    for param in param_iter:
        params.append(param)
    params_df = pd.DataFrame(params, columns=list(param_dict.keys()))
    return params_df


def single_cv_run(history_df, metrics, param_dict):
    mdl = Prophet(**param_dict)
    mdl.fit(history_df)
    df_cvl = cross_validation(mdl, horizon='72 hours')
    df_perf = performance_metrics(df_cvl).mean().to_frame().T
    df_perf['params'] = str(param_dict)
    df_perf = df_perf.loc[:, metrics]
    return df_perf


def store_best_param(df: pd.DataFrame, result_filename: str, param_grid: dict):
    metrics = [
        # 'horizon',
        # 'rmse',
        'mape',
        'params'
    ]
    results = []
    params_df = create_param_combinations(**param_grid)

    for param in params_df.values:
        param_dict = dict(zip(params_df.keys(), param))
        cv_df = single_cv_run(df, metrics, param_dict)
        results.append(cv_df)
    results_df = pd.concat(results).reset_index(drop=True)
    best_param = results_df.loc[results_df['mape'] == min(results_df['mape']), ['params']]
    best_param.to_csv(result_filename)


def start(plant_data_id: str = '43c311e2279f4dd2afce8bbcff62371d', measurement: str = 'humidity'):
    param_grid = {
                'changepoint_prior_scale': [
                    0.001,
                    0.005,
                    0.05,
                    # 0.5,
                    # 5,
                ],
                'changepoint_range': [
                    0.8,
                    # 0.85,
                    0.9,
                ],
                'seasonality_prior_scale': [
                    0.1,
                    0.5,
                    1,
                    # 10.0
                ],
                'seasonality_mode': [
                    # 'multiplicative',
                    'additive'
                ],
                # 'holidays_prior_scale': [0.1, 1, 10.0, ],
                # 'growth': ['linear', 'logistic'],
                # 'yearly_seasonality': [5, 10, 20, ]
              }

    df = pd.read_sql(sql=PlantDataModel.query.filter_by(plant_id=plant_data_id)
                     .order_by(PlantDataModel.creation_date).statement,
                     con=db.engine)

    df['dht_humidity'] = df['dht_humidity']
    df['humidity'] = df[['humidity_1', 'humidity_2', 'humidity_3']].median(axis=1)
    df['luminosity'] = df[['luminosity_1', 'luminosity_2']].mean(axis=1)
    df['temperature'] = df[['temperature', 'dht_temperature']].mean(axis=1)

    df['ds'] = df['creation_date']
    df['y'] = df[measurement]

    result_filename = f'result_{measurement}_{plant_data_id}.csv'

    store_best_param(df, result_filename, param_grid)
