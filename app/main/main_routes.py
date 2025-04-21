from flask import render_template, flash, redirect, url_for, request #,abort, session

from flask_login import current_user #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
#from app.models import db, User
from app.main import bp
#import datetime
#from sqlalchemy import text


@bp.route('/')
@bp.route('/index')
def home():  # Main home page
    if not current_user.is_authenticated:
      return redirect(url_for('.login'))  # Redirect to login page if not logged in
    
    return render_template('index.html') 

