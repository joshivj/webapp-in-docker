from flask import Flask, Blueprint
from dotenv import load_dotenv
from redis import Redis

from hub.routes import bp


def create_app():
    load_dotenv()
    app = Flask(__name__)
    redis = Redis(host='redis', port=6379)

    app.config.from_pyfile('config.py')

    api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
    api_bp.register_blueprint(bp)
    app.register_blueprint(api_bp)

    @app.route('/')
    def hello_geek():
        redis.incr('hits')
        counter = str(redis.get('hits'), 'utf-8')
        return "<h1>Hello from Flask & Docker</h2>. This webpage has been viewed " + counter + " time(s)"

    return app
