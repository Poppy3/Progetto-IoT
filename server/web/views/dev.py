"""DEVELOPMENT ONLY"""

from flask import Blueprint, request

from ..scripts import find_prophet_hyperparams as find_hyperparams

dev_bp = Blueprint('dev', __name__, url_prefix='/dev/scripts')


@dev_bp.route('/find_prophet_hyperparams')
def find_prophet_hyperparams():
    """/dev/scripts/find_prophet_hyperparams?plant_data_id=43c311e2279f4dd2afce8bbcff62371d&measurement=humidity"""
    measurement = request.args.get('measurement', default='humidity')
    plant_data_id = request.args.get('plant_data_id', default='43c311e2279f4dd2afce8bbcff62371d')

    find_hyperparams.start(plant_data_id=plant_data_id, measurement=measurement)

    return 'Finished. Check filesystem for result.'
