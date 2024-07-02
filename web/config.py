import os


DEBUG = True
DEVELOPMENT = True
SECRET_KEY = os.environ.get('SECRET_KEY')
FLASK_HTPASSWD_PATH = os.environ.get('FLASK_HTPASSWD_PATH')
FLASK_SECRET = SECRET_KEY
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PWD = os.environ.get('DB_PWD')
DB_PORT = os.environ.get('DB_PORT')
CONNECTION_STRING = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} " \
                                 f"password={DB_PWD} port={DB_PORT}"

