from flask import render_template, flash, redirect, url_for, request, abort #,session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, WorkSpace
from app.main import bp
#import datetime
#from sqlalchemy import text


@bp.route('/workspaces')
@login_required
def workspaces():  # Main home page:
    workspaces = WorkSpace.query.all()

    return render_template('workspaces.html',spaces = workspaces)

@bp.route('/workspace/<id>') 
@login_required
def show_workspace(id):
   workspace = WorkSpace.query.filter_by(id=id).first()
   if not workspace:
      abort(403)
   return render_template('show_workspace.html',workspace = workspace)
