from flask import Blueprint, render_template


main = Blueprint('main', __name__)


@main.route('/')
def main_index():
    title = 'Main'
    return render_template('base.html', title=title)
