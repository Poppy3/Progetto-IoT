from fbprophet import Prophet
import pandas as pd

HOSTED_APP_URL = 'https://iotproject.eu.pythonanywhere.com'
API_PLANT_DATA = '/api/v1/plant_data'

df_orig = pd.read_json(HOSTED_APP_URL + API_PLANT_DATA)

df = df_orig
df = df.drop(range(1719, 2000))
df = df.iloc[12:]

humidity = df[['creation_date', 'humidity_1', 'humidity_2', 'humidity_3']]

# 1718 == ok
# 1719 == garbage

# 1999 == garbage
# 2000 == ok

import pystan
model_code = 'parameters {real y;} model {y ~ normal(0,1);}'
model = pystan.StanModel(model_code=model_code)  # this will take a minute
y = model.sampling(n_jobs=1).extract()['y']
print(f'y.mean() = {y.mean()}')  # should be close to 0


prophet_df = pd.DataFrame(columns=['ds', 'y'])
prophet_df['ds'] = pd.to_datetime(humidity['creation_date'])
prophet_df['y'] = humidity[['humidity_1', 'humidity_2', 'humidity_3']].median(axis=1)
# Median is the better choice since the datapoints to average are only 3

# define the model
model = Prophet()
# fit the model
model.fit(prophet_df)

print("checkpoint")

future = model.make_future_dataframe(periods=100, freq='H')
print(future.tail())
