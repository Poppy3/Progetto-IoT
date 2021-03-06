################################################################################
# DEVELOPMENT file usato per testare le funzioni relative a fbprophet:
# il modello di facebook per forecasting di timeseries
#
# seguite le istruzioni mostrate in
# https://machinelearningmastery.com/time-series-forecasting-with-prophet-in-python/
################################################################################

# local
# -- EMPTY --

# standard libraries
import fbprophet
from matplotlib import pyplot
import pandas as pd
from sklearn.metrics import mean_absolute_error


if __name__ == '__main__':
    print(f'prophet version: {fbprophet.__version__}')

    # load data
    path = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-car-sales.csv'
    df = pd.read_csv(path, header=0)
    # summarize shape
    print(df.shape)
    # show first few rows
    print(df.head())

    # plot the time series
    df.plot()
    pyplot.show()

    # prepare expected column names
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])

    # define the model
    model = fbprophet.Prophet()
    # fit the model
    model.fit(df)

    # quick validity check
    # define the period for which we want a prediction (within data points)
    future = list()
    for i in range(1, 13):
        date = '1968-%02d' % i
        future.append([date])
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds'] = pd.to_datetime(future['ds'])
    # use the model to make a forecast
    forecast = model.predict(future)
    # summarize the forecast
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
    # plot forecast
    model.plot(forecast)
    pyplot.show()

    # real prediction
    # define the period for which we want a prediction (outside data points)
    future = list()
    for i in range(1, 13):
        date = '1969-%02d' % i
        future.append([date])
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds'] = pd.to_datetime(future['ds'])
    # use the model to make a forecast
    forecast = model.predict(future)
    # summarize the forecast
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
    # plot forecast
    model.plot(forecast)
    pyplot.show()

    # with hold-out test
    # define the period for which we want a prediction
    future = list()
    for i in range(1, 13):
        date = '1968-%02d' % i
        future.append([date])
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds'] = pd.to_datetime(future['ds'])
    # use the model to make a forecast
    forecast = model.predict(future)
    # calculate MAE between expected and predicted values for december
    y_true = df['y'][-12:].values
    y_pred = forecast['yhat'].values
    mae = mean_absolute_error(y_true, y_pred)
    print('MAE: %.3f' % mae)
    # plot expected vs actual
    pyplot.plot(y_true, label='Actual')
    pyplot.plot(y_pred, label='Predicted')
    pyplot.legend()
    pyplot.show()
