from flask import Blueprint


plant_type_bp = Blueprint('plant_type', __name__, url_prefix='/plant_type')


@plant_type_bp.route('/')
@plant_type_bp.route('/index')
def plant_type_bp_index():
    return 'plant_type_bp index'
