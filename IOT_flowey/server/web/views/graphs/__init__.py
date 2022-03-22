from ...models import PlantTypeModel, PlantDataModel, db
from .utils import prepare_prophet_df, fit_and_predict, filter_time_window, predict, find_start_date
from flask import Blueprint, render_template, abort, request
from sqlalchemy.exc import OperationalError
import pandas as pd


graphs_bp = Blueprint('graphs', __name__, url_prefix='/graphs')


@graphs_bp.route('/')
def list_all():
    try:
        plant_data = PlantDataModel.query.distinct(PlantDataModel.plant_id).all()

        plants = {
            p.plant_id: f'{(PlantTypeModel.query.get(p.plant_type_id)).name} - {p.gateway_id}'
            for p in plant_data
        }

    except OperationalError:
        plants = None

    return render_template('graphs/list.html',
                           title='Graphs',
                           plants=plants)


@graphs_bp.route('/id/<plant_data_id>')
def details(plant_data_id):
    try:
        time_window = request.args.get('time_window')
        if time_window not in ['all_time', 'last_month', 'last_week']:
            time_window = 'last_week'

        show_predict = request.args.get('predict', default='false').lower() == 'true'

        df = pd.read_sql(sql=PlantDataModel.query.filter_by(plant_id=plant_data_id)
                         .order_by(PlantDataModel.creation_date).statement,
                         con=db.engine)
        if df.empty:
            abort(404)

        start_date = find_start_date(df, time_window)

        plant_info = df.iloc[0]  # getting first row of dataframe
        plant_type_id = int(plant_info['plant_type_id'])
        plant_type = PlantTypeModel.query.get_or_404(plant_type_id)

        df['humidity_median'] = df[['humidity_1', 'humidity_2', 'humidity_3']].median(axis=1)
        df['luminosity_mean'] = df[['luminosity_1', 'luminosity_2']].mean(axis=1)
        df['temperature_mean'] = df[['temperature', 'dht_temperature']].mean(axis=1)

        df_filtered = filter_time_window(df, start_date, ds_col_name='creation_date')

        labels = df_filtered['creation_date']

        chart_data = {
            'dht_humidity': {
                'labels': labels,
                'datasets': [
                    {
                        # 'color': '#126e82',
                        'label': 'DHT Humidity Sensor',
                        'data': df_filtered['dht_humidity'],
                    },
                ],
            },
            'humidity': {
                'labels': labels,
                'datasets': [
                    {
                        # 'color': '#8c0000',
                        'label': 'Humidity Median',
                        'data': df_filtered['humidity_median'],
                    },
                    {
                        # 'color': '#864000',
                        'label': 'Sensor 1',
                        'data': df_filtered['humidity_1'],
                        'hidden': 'true',
                    },
                    {
                        # 'color': '#d44000',
                        'label': 'Sensor 2',
                        'data': df_filtered['humidity_2'],
                        'hidden': 'true',
                    },
                    {
                        # 'color': '#ff7a00',
                        'label': 'Sensor 3',
                        'data': df_filtered['humidity_3'],
                        'hidden': 'true',
                    },
                ],
                'min': plant_type.humidity_min,
                'max': plant_type.humidity_max,
            },
            'temperature': {
                'labels': labels,
                'datasets': [
                    {
                        # 'color': '#876e82',
                        'label': 'Temperature Mean',
                        'data': df_filtered['temperature_mean'],
                    },
                    {
                        # 'color': '#126e82',
                        'label': 'DHT Temperature Sensor',
                        'data': df_filtered['dht_temperature'],
                        'hidden': 'true',
                    },
                    {
                        # 'color': '#51c4d3',
                        'label': 'Termoresistor Sensor',
                        'data': df_filtered['temperature'],
                        'hidden': 'true',
                    },
                ],
                'min': plant_type.temperature_min,
                'max': plant_type.temperature_max,
            },
            'luminosity': {
                'labels': labels,
                'datasets': [
                    {
                        # 'color': '#436f8a',
                        'label': 'Luminosity Mean',
                        'data': df_filtered['luminosity_mean'],
                    },
                    {
                        # 'color': '#bac964',
                        'label': 'Sensor 1',
                        'data': df_filtered['luminosity_1'],
                        'hidden': 'true',
                    },
                    {
                        # 'color': '#438a5e',
                        'label': 'Sensor 2',
                        'data': df_filtered['luminosity_2'],
                        'hidden': 'true',
                    },
                ],
                'min': plant_type.luminosity_min,
                'max': plant_type.luminosity_max,
            },
        }

        if show_predict:
            try:
                prediction_dht_humidity = predict(plant_data_id, 'dht_humidity')
            except FileNotFoundError:
                prediction_dht_humidity = fit_and_predict(plant_data_id,
                                                          prepare_prophet_df(df, 'dht_humidity'),
                                                          'dht_humidity')
            try:
                prediction_humidity = predict(plant_data_id, 'humidity')
            except FileNotFoundError:
                prediction_humidity = fit_and_predict(plant_data_id,
                                                      prepare_prophet_df(df, 'humidity_median'),
                                                      'humidity')
            try:
                prediction_luminosity = predict(plant_data_id, 'luminosity')
            except FileNotFoundError:
                prediction_luminosity = fit_and_predict(plant_data_id,
                                                        prepare_prophet_df(df, 'luminosity_mean'),
                                                        'luminosity')
            try:
                prediction_temperature = predict(plant_data_id, 'temperature')
            except FileNotFoundError:
                prediction_temperature = fit_and_predict(plant_data_id,
                                                         prepare_prophet_df(df, 'temperature_mean'),
                                                         'temperature')

            prediction_dht_humidity = filter_time_window(prediction_dht_humidity, start_date)
            prediction_humidity = filter_time_window(prediction_humidity, start_date)
            prediction_luminosity = filter_time_window(prediction_luminosity, start_date)
            prediction_temperature = filter_time_window(prediction_temperature, start_date)

            labels = prediction_dht_humidity['ds']

            chart_data['dht_humidity']['labels'] = labels
            chart_data['humidity']['labels'] = labels
            chart_data['luminosity']['labels'] = labels
            chart_data['temperature']['labels'] = labels

            chart_data['dht_humidity']['datasets'].insert(0, {
                'color': '#6610f2',
                'label': 'Prediction',
                'data': prediction_dht_humidity['yhat'],
            })
            chart_data['humidity']['datasets'].insert(0, {
                'color': '#6610f2',
                'label': 'Prediction',
                'data': prediction_humidity['yhat'],
            })
            chart_data['luminosity']['datasets'].insert(0, {
                'color': '#6610f2',
                'label': 'Prediction',
                'data': prediction_luminosity['yhat'],
            })
            chart_data['temperature']['datasets'].insert(0, {
                'color': '#6610f2',
                'label': 'Prediction',
                'data': prediction_temperature['yhat'],
            })

        return render_template('graphs/details.html',
                               title=f'Graphs for {plant_type.name} - {plant_info.gateway_id}',
                               plant_type=plant_type,
                               plant_info=plant_info,
                               chart_data=chart_data,)
    except OperationalError:
        abort(500)


@graphs_bp.route('/<measure>')
def measurement(measure):
    if measure == 'dht_humidity':
        measure_title = 'Air humidity'
        data_columns = ['dht_humidity']
    elif measure == 'humidity':
        measure_title = 'Terrain humidity'
        data_columns = ['humidity_1', 'humidity_2', 'humidity_3']
    elif measure == 'luminosity':
        measure_title = 'Luminosity'
        data_columns = ['luminosity_1', 'luminosity_2']
    elif measure == 'temperature':
        measure_title = 'Temperature'
        data_columns = ['dht_temperature', 'temperature']
    else:
        abort(404)
        measure_title = ''  # only here since the IDE complains otherwise
        data_columns = []   # only here since the IDE complains otherwise

    try:
        time_window = request.args.get('time_window')
        if time_window not in ['all_time', 'last_month', 'last_week']:
            time_window = 'last_week'

        show_predict = request.args.get('predict', default='false').lower() == 'true'

        plants = {}
        df = pd.read_sql(sql=PlantDataModel.query
                         .order_by(PlantDataModel.creation_date).statement,
                         con=db.engine)
        if df.empty:
            abort(404)

        start_date = find_start_date(df, time_window)

        if len(data_columns) == 3:
            df['measure'] = df[data_columns].median(axis=1)
        else:
            df['measure'] = df[data_columns].mean(axis=1)

        # todo remove
        # df2 = df.copy()
        # df2['gateway_id'] = 'GATEWAY_ID'
        # df2['plant_id'] = 'PLANT_ID'
        # df2['creation_date'] = df2['creation_date'] + pd.DateOffset(hours=3)
        # df2['measure'] = df2['measure'].divide(1.1)
        # df = pd.concat([df, df2], ignore_index=True)
        # df = df.sort_values('creation_date')
        # end todo remove

        df_filtered = filter_time_window(df, start_date, ds_col_name='creation_date').copy()

        labels = df_filtered['creation_date']

        for _, row in df_filtered.groupby(['plant_id', 'gateway_id'], as_index=False).all().iterrows():
            plant_id = row['plant_id']
            gateway_id = row['gateway_id']

            row_index = df_filtered['gateway_id'] == gateway_id
            df_filtered[f'{measure}_{gateway_id}'] = df_filtered.loc[row_index, 'measure']
            df_filtered[f'{measure}_{gateway_id}'].fillna(value='NaN', inplace=True)

            plants[plant_id] = f'{(PlantTypeModel.query.get(row["plant_type_id"])).name} - {gateway_id}'

        chart_data = {
            measure: {
                'labels': labels,
                'datasets': [
                    {
                        'label': gateway_id,
                        'data': df_filtered[f'{measure}_{gateway_id}'],
                        'hidden': 'true' if show_predict else 'false',
                    }
                    for gateway_id in df_filtered['gateway_id'].unique()
                ],
            },
        }

        if show_predict:
            for _, row in df_filtered.groupby(['plant_id', 'gateway_id'], as_index=False).all().iterrows():
                plant_id = row['plant_id']
                gateway_id = row['gateway_id']
                try:
                    prediction = predict(plant_id, measure)
                except FileNotFoundError:
                    prediction = fit_and_predict(plant_id,
                                                 prepare_prophet_df(df, 'measure'),
                                                 measure)

                prediction = filter_time_window(prediction, start_date)
                chart_data[measure]['labels'] = prediction['ds']
                chart_data[measure]['datasets'].append({
                    'label': f'Prediction {gateway_id}',
                    'data': prediction['yhat'],
                })

        return render_template('graphs/measurement.html',
                               title=f'{measure_title} graphs',
                               chart_title=measure_title,
                               chart_data=chart_data,
                               measure=measure,
                               plants=plants,
                               )

    except OperationalError:
        abort(500)
