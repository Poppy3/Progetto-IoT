from ..config import FBPROPHET_HYPERPARAMS_PATH, FBPROPHET_MODELS_PATH
from fbprophet import Prophet
from fbprophet.serialize import model_from_json, model_to_json
from typing import Optional
import json
import pandas as pd


def load_model(plant_data_id: str, measurement: str, path: str = FBPROPHET_MODELS_PATH) -> Optional[Prophet]:
    try:
        df = pd.read_csv(path)
        row_indexer = (df['plant_data_id'] == plant_data_id) & (df['measurement'] == measurement)
        model_string = df.loc[row_indexer, 'model'].iloc[0]
        return model_from_json(json.loads(model_string))
    except (FileNotFoundError, IndexError):
        return None


def save_model(plant_data_id: str, measurement: str, model: Prophet, path: str = FBPROPHET_MODELS_PATH):
    model_string = json.dumps(model_to_json(model))
    new_row = {
        'plant_data_id': plant_data_id,
        'measurement': measurement,
        'model': model_string,
    }
    try:
        df = pd.read_csv(path)
        row_indexer = (df['plant_data_id'] == plant_data_id) & (df['measurement'] == measurement)
        if not df.loc[row_indexer].empty:
            df.loc[row_indexer, 'model'] = model_string
        else:
            df = df.append(new_row, ignore_index=True)
        df.to_csv(path, index=False)
    except FileNotFoundError:
        df = pd.DataFrame([new_row], columns=['plant_data_id', 'measurement', 'model'])
        df.to_csv(path, index=False)


def save_hyperparams(plant_data_id: str, measurement: str, hyperparams: dict, path: str = FBPROPHET_HYPERPARAMS_PATH):
    hyperparams_string = json.dumps(hyperparams)
    new_row = {
        'plant_data_id': plant_data_id,
        'measurement': measurement,
        'hyperparams': hyperparams_string,
    }
    try:
        df = pd.read_csv(path)
        row_indexer = (df['plant_data_id'] == plant_data_id) & (df['measurement'] == measurement)
        if not df.loc[row_indexer].empty:
            df.loc[row_indexer, 'hyperparams'] = hyperparams_string
        else:
            df = df.append(new_row, ignore_index=True)
        df.to_csv(path, index=False)
    except FileNotFoundError:
        df = pd.DataFrame([new_row], columns=['plant_data_id', 'measurement', 'hyperparams'])
        df.to_csv(path, index=False)


def main__save_hyperparams():
    """ FOR TEST ONLY """
    plant_data_id = '43c311e2279f4dd2afce8bbcff62371d'
    measurement = 'luminosity'
    hyperparams = {
        'changepoint_prior_scale': 0.001,
        'changepoint_range': 0.9,
        'seasonality_prior_scale': 0.5,
        'seasonality_mode': 'additive',
    }
    save_hyperparams(plant_data_id, measurement, hyperparams, 'hyperparams.csv')


if __name__ == '__main__':
    main__save_hyperparams()

