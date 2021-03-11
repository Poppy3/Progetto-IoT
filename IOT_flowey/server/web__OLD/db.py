################################################################################
# Define and Access the Database.
# See: https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
################################################################################

# local
import config as cfg
from database_connector import DatabaseConnector

# standard libraries
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        DatabaseConnector().connection
        g.db = DatabaseConnector().connection
        # g.db.row_factory = sqlite3.Row  # MySql.connection.cursor(dictionary=True) dovrebbe
                                          # ritornare le righe gia come dict
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # with current_app.open_resource('schema.sql') as f:  # Commentato visto che non DOVREBBE servire.
    #     db.executescript(f.read().decode('utf8'))


# Commentato visto che non DOVREBBE servire.
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    #app.cli.add_command(init_db_command)
    init_db()  # aggiunto al posto del comando sopra
