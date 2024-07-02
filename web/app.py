from flask import Flask, Blueprint
from dotenv import load_dotenv

from hub.routes import bp
from extras.redis_helper import RedisHelper


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
    api_bp.register_blueprint(bp)
    app.register_blueprint(api_bp)
    redis_helper_obj = RedisHelper()
    app.redis_client = redis_helper_obj

    @app.route('/')
    def hello_geek():
        redis_helper_obj.incrementer('hits')
        counter = str(redis_helper_obj.get_value('hits'))
        return "<h1>Hello from Flask & Docker.</h2> This webpage has been viewed " + counter + " time(s)"

    return app
