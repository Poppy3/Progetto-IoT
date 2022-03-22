from ..models.plant_data import PlantDataModel
from ..models.plant_type import PlantTypeModel
from ..utils import human_readable_time
from telegram.utils.helpers import escape_markdown
from typing import Tuple

import numpy as np
import pandas as pd


def escape_markdown_V2(text: str, version: int = 2, entity_type: str = None) -> str:
    return escape_markdown(text=text, version=version, entity_type=entity_type)


def get_keyboard_layout(entries: list, esc_markdown: bool = False) -> list:
    n = len(entries)
    if n <= 0:
        return []

    max_width = 3  # more than three elements in a row can be ugly to see
    if n == 4:
        # 2 rows of 2 elements is nicer than three rows with 2,1,1
        # elements each that would result by using the calculation below
        rows = 2
    else:
        rows = max((n - 1) // max_width + 1, max_width)

    if esc_markdown:
        entries = [escape_markdown_V2(entry) for entry in entries]

    # np.array_split(list, N) splits a list in N sub-lists of (almost) equal length
    return [arr.tolist() for arr in np.array_split(entries, rows)]


def get_faults(dataframe, df_filter, min_val, max_val) -> Tuple[int, int]:
    """return type is a tuple of the form: (<# of less than min_val>, <# of more than max_val>)"""
    min_faults, max_faults = 0, 0

    if min_val is not None or max_val is not None:
        if len(df_filter) == 3:
            values = dataframe[df_filter].median(axis=1)
        else:
            values = dataframe[df_filter].mean(axis=1)

        if min_val is not None:
            min_faults = values[values < min_val].count()
        if max_val is not None:
            min_faults = values[values > max_val].count()

    return min_faults, max_faults


def get_plant_data_report(gateway_id, plant_name, timedelta_seconds: int = 86400):
    plant_data_query = (PlantDataModel.query
                        .filter(PlantDataModel.gateway_id == gateway_id))

    df = pd.read_sql(plant_data_query.statement, plant_data_query.session.bind)

    start_date = df['creation_date'].iloc[-1] + pd.DateOffset(seconds=-timedelta_seconds)
    df = df.loc[df['creation_date'] >= start_date]

    if len(df) == 0:
        return f'No data retrieved during the last {human_readable_time(timedelta_seconds)}'

    plant_type: PlantTypeModel
    plant_type = (PlantTypeModel.query
                  .join(PlantDataModel)
                  .filter(PlantDataModel.gateway_id == gateway_id)
                  .filter(PlantTypeModel.name == plant_name)
                  .first())

    h_faults_min, h_faults_max = get_faults(dataframe=df,
                                            df_filter=[PlantDataModel.humidity_1.key,
                                                       PlantDataModel.humidity_2.key,
                                                       PlantDataModel.humidity_3.key],
                                            min_val=plant_type.humidity_min,
                                            max_val=plant_type.humidity_max)
    l_faults_min, l_faults_max = get_faults(dataframe=df,
                                            df_filter=[PlantDataModel.luminosity_1.key,
                                                       PlantDataModel.luminosity_2.key],
                                            min_val=plant_type.luminosity_min,
                                            max_val=plant_type.luminosity_max)
    t_faults_min, t_faults_max = get_faults(dataframe=df,
                                            df_filter=[PlantDataModel.temperature.key,
                                                       PlantDataModel.dht_temperature.key],
                                            min_val=plant_type.temperature_min,
                                            max_val=plant_type.temperature_max)

    if sum([h_faults_min, h_faults_max, l_faults_min, l_faults_max, t_faults_min, t_faults_max]) == 0:
        return (f' · *Everything* has been __good__ '
                f'during the last {human_readable_time(timedelta_seconds)}')

    if h_faults_min > 5 and h_faults_max > 5:
        h_status = 'both __too damp__ and __too dry__'
    elif h_faults_min > 5:
        h_status = '__too dry__'
    elif h_faults_max > 5:
        h_status = '__too damp__'
    else:
        h_status = '__good__'
    h_status = f'*Humidity* has been {h_status}'

    if l_faults_min > 5 and l_faults_max > 5:
        l_status = 'both __too bright__ and __too dark__'
    elif l_faults_min > 5:
        l_status = '__too dark__'
    elif l_faults_max > 5:
        l_status = '__too bright__'
    else:
        l_status = '__good__'
    l_status = f'*Luminosity* has been {l_status}'

    if t_faults_min > 5 and t_faults_max > 5:
        t_status = 'both __too hot__ and __too cold__'
    elif t_faults_min > 5:
        t_status = '__too cold__'
    elif t_faults_max > 5:
        t_status = '__too hot__'
    else:
        t_status = '__good__'
    t_status = f'*Temperature* has been {t_status}'

    return (f'During the last {human_readable_time(timedelta_seconds)}\n'
            f' · {h_status}\n'
            f' · {l_status}\n'
            f' · {t_status}')
