from .base import db, migrate
from .user import User, ACCESS
from .workspace import WorkSpace
from .slot import Slot


def init_app(app):
    db.init_app(app);
    migrate.init_app(app,db)
