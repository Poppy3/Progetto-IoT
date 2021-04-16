from typing import Tuple
from web.models.plant_data import PlantDataModel
from web.models.plant_type import PlantTypeModel
import pandas as pd
import numpy as np
from pathlib import Path

import timeit


df = pd.read_csv(Path(__file__).with_name('dataframe.csv'))

print(df)

plant_type: PlantTypeModel
# plant_type = (PlantTypeModel.query
#               .join(PlantDataModel)
#               .filter(PlantDataModel.gateway_id == "ARDUINO001")
#               .filter(PlantTypeModel.name == "Geranio")
#               .first())

plant_type = PlantTypeModel(
    name='Geranio',
    humidity_min=40,
    humidity_max=55,
    humidity_tolerance_time=3600,
    luminosity_min=40,
    temperature_max=50,
)


# print(plant_type)


def get_faults(dataframe, df_filter, min_val, max_val) -> Tuple[int, int]:
    """return type is a tuple of the form: (<# of less than min_val>, <# of more than max_val>)"""
    min_faults, max_faults = 0, 0
    if min_val is not None or max_val is not None:
        mean: pd.Series = dataframe[df_filter].mean(axis=1)
        if min_val is not None:  # and min_val is not None
            min_faults = mean.size - np.count_nonzero(mean >= min_val)
        if max_val is not None:  # and max_val is not None
            max_faults = mean.size - np.count_nonzero(mean <= max_val)
    return min_faults, max_faults


def get_faults_number(dataframe: pd.DataFrame, df_filter, min_val, max_val) -> int:
    print(f'\nmin= {min_val} | max= {max_val}')
    if min_val is not None or max_val is not None:
        mean: pd.Series = dataframe[df_filter].mean(axis=1)
        print(mean)
        if max_val is None:  # and min_val is not None
            return mean.size - np.count_nonzero(mean >= min_val)
        if min_val is None:  # and max_val is not None
            return mean.size - np.count_nonzero(mean <= max_val)
        # if and min_val is not None and max_val is not None
        return mean.size - np.count_nonzero(mean.between(min_val, max_val))
    return 0


h_faults = get_faults(dataframe=df,
                            df_filter=[PlantDataModel.humidity_1.key,
                                       PlantDataModel.humidity_2.key,
                                       PlantDataModel.humidity_3.key],
                            min_val=plant_type.humidity_min,
                            max_val=plant_type.humidity_max)
print(h_faults)
l_faults = get_faults(dataframe=df,
                            df_filter=[PlantDataModel.luminosity_1.key,
                                       PlantDataModel.luminosity_2.key],
                            min_val=plant_type.luminosity_min,
                            max_val=plant_type.luminosity_max)
print(l_faults)
t_faults = get_faults(dataframe=df,
                            df_filter=[PlantDataModel.temperature.key,
                                       PlantDataModel.dht_temperature.key],
                            min_val=plant_type.temperature_min,
                            max_val=plant_type.temperature_max)
print(t_faults)


#
#
#
