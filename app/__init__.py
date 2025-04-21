from flask import Flask
from config import Config

def create_app(app_conf_file=None):
    app = Flask(__name__)
    app.config.from_object(Config)           # Default Configurations    

    from app import models
    models.init_app(app)

    from app import main
    main.init_app(app)
    
    from app import cli
    cli.init_app(app)

    return app