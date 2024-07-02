# @todo: introduce design pattern/logger and refactor the code

import psycopg2
import psycopg2.extras

from flask import Blueprint
from flask import current_app as app
from extras.pg_helper import PgHelper

bp = Blueprint('hub', __name__, url_prefix='/hub')


@bp.route('/users/')
def get_users():
    connection_string = app.config.get('CONNECTION_STRING')
    conn = psycopg2.connect(connection_string)
    redis_key = 'list-of-all-users'
    # get value from cache - if it doesn't exists then dump in cache
    print('------------------ getting records from cache ------------------')
    records = app.redis_client.get_value(redis_key)
    if not records:
        # set it in cache
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                pg = PgHelper(curs)
                records = pg.get_all_records('users', ['id', 'username', 'email', 'bio'])
        finally:
            conn.close()
        print('------------------ setting records in cache ------------------')
        app.redis_client.set_value(redis_key, records)
    return records


@bp.route('/users/<int:pk>/')
def get_user_by_pk(pk):
    connection_string = app.config.get('CONNECTION_STRING')
    conn = psycopg2.connect(connection_string)
    redis_key = f'user-detail-{pk}'
    # get value from cache - if it doesn't exists then dump in cache
    print('------------------ getting user from cache ------------------')
    records = app.redis_client.get_value(redis_key)
    if not records:
        # set it in cache
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                pg = PgHelper(curs)
                records = pg.get_record('users', 'id', pk)
                print(records)
        finally:
            conn.close()
        print('------------------ setting user in cache ------------------')
        app.redis_client.set_value(redis_key, records)
    return records


@bp.route('/cache-clear/')
def clear_the_cache():
    redis_client = app.redis_client
    redis_client.invalidate_all_keys_in_db()
    return {"success": True}
