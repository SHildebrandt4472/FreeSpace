from .base import db, migrate
from .user import User, ACCESS, user_skill_table
from .workspace import WorkSpace, workspace_skill_table
from .slot import Slot
from .skill import Skill


def init_app(app):
    db.init_app(app);
    migrate.init_app(app,db)
