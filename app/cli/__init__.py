
from flask import Blueprint

bp = Blueprint('cli', __name__)

def init_app(app):
    app.register_blueprint(bp)

from . import commands
