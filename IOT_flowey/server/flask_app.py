################################################################################
# Flask Application Server
# Qui vengono gestite le pagine del sito web
################################################################################

# local
import config as cfg

# standard libraries
from flask import Flask, Markup, render_template
import random

app = Flask(__name__,
            static_url_path=cfg.FLASK.STATIC_URL_PATH,
            static_folder=cfg.FLASK.STATIC_FOLDER,
            template_folder=cfg.FLASK.TEMPLATE_FOLDER)

app.config['TEMPLATES_AUTO_RELOAD'] = cfg.FLASK.TEMPLATES_AUTO_RELOAD

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

colors_rgba = [
    "rgba(247,70,74,0.8)", "rgba(70,191,189,0.8)", "rgba(253,180,92,0.8)", "rgba(254,220,186,0.8)",
    "rgba(254,220,186,0.8)", "rgba(221,221,221,0.8)", "rgba(171,202,188,0.8)", "rgba(65,105,225,0.8)",
    "rgba(199,21,133,0.8)", "rgba(255,69,0,0.8)", "rgba(254,220,186,0.8)", "rgba(70,191,189,0.8)"]


# inserisce automagicamente una chiave 'randint'
# nel dictionary context di ogni render_template
@app.context_processor
def utility_randint():
    def randint(a, b):
        return random.randint(a, b)
    return dict(randint=randint)


@app.route('/')
def index():
    return render_template('index.html', title='Index')


@app.route('/bar')
def bar():
    bar_labels = labels
    bar_values = values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000,
                           labels=bar_labels, values=bar_values)


@app.route('/line')
def line():
    line_labels = labels
    line_values = values
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000,
                           labels=line_labels, values=line_values)


@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    pie_colors = colors
    #pie_colors = colors_rgba
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000,
                           values=pie_values, labels=pie_labels, colors=pie_colors)


@app.route('/time')
def time():
    return render_template('time_chart.html', title='Time Chart Example')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
