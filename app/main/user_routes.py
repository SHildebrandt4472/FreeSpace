from flask import render_template, flash, redirect, url_for, request, abort #,session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, User, Skill
from app.main import bp
#import datetime
#from sqlalchemy import text
from .user_forms import UserEditForm, ChangePasswordForm


@bp.route('/users')
@login_required
def users():  # Main home page:
    if not current_user.is_manager():
      abort(403)
      
    users = User.query.order_by(User.display_name)
    return render_template('users.html',users = users)

@bp.route('/user/new', methods=['GET', 'POST'],  defaults={'id':None})
@bp.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    print("id", id)
    print("user", current_user.id)
    if not current_user.is_admin():
      if id != current_user.id:
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
        reset_password = form.reset_password.data and user != current_user
        if reset_password:
          user.password_hash = ''

        if not user.id:               
          db.session.add(user)
        db.session.commit()        
        if reset_password:
          flash(f"Password has been reset for user '{user.username}'")
        else:
          flash('Your changes have been saved.')  

        return redirect(url_for('.show_user', id=user.id))
    elif request.method == 'GET':
        form.id.data = user.id
        form.username.data = user.username
        form.display_name.data = user.display_name
        form.email.data = user.email
        form.access.data = user.access        
    return render_template('user_edit.html', title=title, form=form, user=user)

@bp.route('/user/<id>') 
@login_required
def show_user(id):
   user = User.query.get_or_404(id)
   return render_template('show_user.html',user = user)

@bp.route('/user/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
   if not current_user.is_admin():
      abort(403)

   user = User.query.get_or_404(id)

   if user.id == current_user.id:   
      flash('You cannot delete yourself', 'error')
      return redirect(url_for('.show_user', id=user.id))          
   
   db.session.delete(user)
   db.session.commit()
   return redirect(url_for('.users'))


@bp.route('/user/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
      if current_user.password_hash and not current_user.check_password(form.current_password.data):
        flash('Your current password was invalid. Please try again','error')
        return redirect(url_for('.change_password'))
      if form.password.data:
        first_password = not current_user.password_hash
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('.home'))        
    return render_template('user_change_password.html', title='Change Password', form=form)

@bp.route('/user/<user_id>/edit_skills')
@login_required
def edit_user_skills(user_id):
  if not current_user.is_manager():
    abort(403)

  user = User.query.get_or_404(user_id)
  all_skills = Skill.query.all()

  return render_template('user_edit_skills.html', title=f'Edit Skills for {user.name()}', user=user, all_skills=all_skills)

@bp.route('/user/<user_id>/add_skill/<skill_id>', methods=['POST'])
@login_required
def add_user_skill(user_id, skill_id):
  if not current_user.is_manager():
    abort(403)

  user = User.query.get_or_404(user_id)
  skill = Skill.query.get_or_404(skill_id)
  if not user.has_skill(skill):
    user.skills.append(skill)
    db.session.commit()
  
  return redirect(url_for('.edit_user_skills', user_id = user.id))       

@bp.route('/user/<user_id>/remove_skill/<skill_id>', methods=['POST'])
@login_required
def remove_user_skill(user_id, skill_id):
  if not current_user.is_manager():
    abort(403)

  user = User.query.get_or_404(user_id)
  skill = Skill.query.get_or_404(skill_id)
  if user.has_skill(skill):
    user.skills.remove(skill)
    db.session.commit()
  
  return redirect(url_for('.edit_user_skills', user_id = user.id))      