from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config

limiter = Limiter(get_remote_address)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    limiter.init_app(app)
    return app