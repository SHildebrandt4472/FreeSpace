from flask import render_template, flash, redirect, url_for, request, abort, session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, WorkSpace, Slot
from app.main import bp
import datetime
#from sqlalchemy import text
from .workspace_forms import WorkspaceEditForm



@bp.route('/workspaces')
@login_required
def workspaces():  # Main home page:
    workspaces = WorkSpace.query.all()

    return render_template('workspaces.html',spaces = workspaces)

@bp.route('/workspace/<id>', defaults = {'day':None} ) 
@bp.route('/workspace/<id>/<date:day>') 
@login_required
def show_workspace(id,day):
   workspace = WorkSpace.query.get_or_404(id)

   if not day:
      day = datetime.date.today()
   start_date = day - datetime.timedelta(days=day.weekday())  # calculate date of monday of current week
   end_date = start_date + datetime.timedelta(days=7)
   #dates = []
   
   daily_slots = []
   for i in range(7):
      slots = []
      daily_slots.append({'date'  : start_date + datetime.timedelta(days=i),
                          'slots' : slots})
      #dates.append(start_date + datetime.timedelta(days=i))

   for slot in workspace.slots.filter(Slot.start_time.between(start_date,end_date)):
         dow = slot.start_time.weekday()
         daily_slots[dow]['slots'].append(slot)

   next_url = url_for('.show_workspace',id=id, day=end_date)
   prev_url = url_for('.show_workspace',id=id, day=start_date-datetime.timedelta(days=1))
   session['back_to'] = url_for('.show_workspace', id=id, date=slot.start_time.date())
   return render_template('show_workspace.html',workspace = workspace, daily_slots = daily_slots, prev_url = prev_url, next_url = next_url)

@bp.route('/workspace/new', defaults={'id':None})
@bp.route('/workspace/<id>/edit')
@login_required
def edit_workspace(id):
   if not current_user.is_admin():
      abort(403)   
   
   if id:
      workspace = WorkSpace.query.get_or_404(id)
      title = "Edit workspace"
   
   else:
      workspace = WorkSpace()
      title = "New workspace"

   form = WorkspaceEditForm()
   form.name.data = workspace.name
   form.description.data = workspace.description
   form.location.data = workspace.location
   form.status.data = workspace.status
   action = url_for('.update_workspace',id=workspace.id)
   return render_template('edit_workspace.html', title=title, action=action, form=form)
   
   

@bp.route('/workspace/add', methods=['POST'], defaults={'id':None})
@bp.route('/workspace/<id>/update', methods=['POST'])
@login_required
def update_workspace(id):
   if not current_user.is_admin():
      abort(403)
      
   if id:
      workspace = WorkSpace.query.get_or_404(id)
      title = "Edit workspace"
   else:
      workspace = WorkSpace()
      title = "New workspace"

   form = WorkspaceEditForm()
   if form.validate_on_submit():
        workspace.name = form.name.data
        workspace.description = form.description.data
        workspace.location = form.location.data
        workspace.status = form.status.data

        if not workspace.id:
            db.session.add(workspace)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.workspaces'))
   return render_template('edit_workspace.html', title=title, form=form)

@bp.route('/workspace/<id>/delete', methods=['POST'])
@login_required
def delete_workspace(id):
   if not current_user.is_admin():
      abort(403)

   workspace = WorkSpace.query.get_or_404(id)
   db.session.delete(workspace)
   db.session.commit()
   return redirect(url_for('.workspaces'))