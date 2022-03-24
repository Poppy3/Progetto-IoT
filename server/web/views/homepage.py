from flask import Blueprint, render_template

homepage_bp = Blueprint('homepage', __name__)


@homepage_bp.route('/index')
@homepage_bp.route('/')
def index():
    title = 'Flowey - Homepage'
    return render_template('homepage/homepage.html', title=title)
