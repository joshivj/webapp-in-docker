# @todo: introduce factory pattern and refactor the code

import psycopg2
import psycopg2.extras

from flask import Blueprint
from flask import current_app as app
from extras.pg_helper import PgHelper

bp = Blueprint('hub', __name__, url_prefix='/hub')


@bp.route('/users/')
def get_users():
    connection_string = app.config.get('CONNECTION_STRING')
    print(connection_string)
    conn = psycopg2.connect(connection_string)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            pg = PgHelper(curs)
            records = pg.get_all_records('users', ['id', 'username', 'email', 'bio'])
    finally:
        conn.close()
    return records


@bp.route('/users/<int:pk>/')
def get_user_by_pk(pk):
    connection_string = app.config.get('CONNECTION_STRING')
    conn = psycopg2.connect(connection_string)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            pg = PgHelper(curs)
            records = pg.get_record('users', 'id', pk)
    finally:
        conn.close()
    return records
