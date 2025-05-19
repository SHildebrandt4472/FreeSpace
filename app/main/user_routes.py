from flask import render_template, flash, redirect, url_for, request, abort #,session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, User
from app.main import bp
#import datetime
#from sqlalchemy import text
from .user_forms import UserEditForm


@bp.route('/users')
@login_required
def users():  # Main home page:
    if not current_user.is_admin():
      abort(403)
      
    users = User.query.all()

    return render_template('users.html',users = users)

@bp.route('/user/new', methods=['GET', 'POST'],  defaults={'id':None})
@bp.route('/user/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not current_user.is_admin():
      abort(403)

    if id:
      user = User.query.get_or_404(id)
      title = "Edit User"
    else:
      user = User()
      title = "New User"

    form = UserEditForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data.lower()
        user.display_name = form.display_name.data
        if form.email.data != user.email:
          user.email = form.email.data
          user.email_verified = False
        if user != current_user:           # Can't change your own access level
          user.access = form.access.data
        #reset_password = form.reset_password.data and user != current_user
        #if reset_password:
        #  user.password_hash = ''

        if not user.id:               
          db.session.add(user)
        db.session.commit()
        flash('Your changes have been saved.')
        #if reset_password:
        #  flash(f"Password has been reset for user '{user.username}'")

        return redirect(url_for('.users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.display_name.data = user.display_name
        form.email.data = user.email
        form.access.data = user.access
    return render_template('user_edit.html', title=title, form=form)

@bp.route('/user/<id>') 
@login_required
def show_user(id):
   user = User.query.get_or_404(id)
   return render_template('show_user.html',user = user)

@bp.route('/user/<id>/delete', methods=['POST'])
@login_required
def delete_user(id):
   if not current_user.is_admin():
      abort(403)

   user = User.query.get_or_404(id)
   db.session.delete(user)
   db.session.commit()
   return redirect(url_for('.users'))