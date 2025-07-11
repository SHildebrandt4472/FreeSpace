from flask import render_template, flash, redirect, url_for, request, abort, session, current_app

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, WorkSpace, Slot, Skill
from app.main import bp
import datetime
#from sqlalchemy import text
from .workspace_forms import WorkspaceEditForm
import os



@bp.route('/workspaces')
@login_required
def workspaces():  # Main home page:
    workspaces = WorkSpace.query.order_by('name').all()
    usable_workspaces = []
    other_workspaces = []
    for workspace in workspaces:
      if current_user.has_skills_for(workspace):
         usable_workspaces.append(workspace)
      else:
         other_workspaces.append(workspace)
    session['back_to'] = url_for('.workspaces')
    return render_template('workspaces.html',usable_workspaces = usable_workspaces, other_workspaces=other_workspaces, page='Workspaces')

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

   edit_slots = current_user.is_manager() and request.args.get('edit')
   edit_slots_url = url_for('.show_workspace',id=id, day=day, edit=1)
   next_url = url_for('.show_workspace',id=id, day=end_date, edit=edit_slots)
   prev_url = url_for('.show_workspace',id=id, day=start_date-datetime.timedelta(days=1), edit=edit_slots)
   session['back_to'] = url_for('.show_workspace', id=id, day=day, edit=edit_slots)
   return render_template('show_workspace.html',workspace = workspace, daily_slots = daily_slots, prev_url = prev_url, next_url = next_url, edit_slots=edit_slots, edit_slots_url=edit_slots_url, day=day)

@bp.route('/workspace/new', defaults={'id':None})
@bp.route('/workspace/<id>/edit')
@login_required
def edit_workspace(id):
   if not current_user.is_manager():
      abort(403)   
   
   form = WorkspaceEditForm()
   if id:
      workspace = WorkSpace.query.get_or_404(id)
      title = "Edit workspace"
      form.submit.label.text = "Update"
   
   else:
      workspace = WorkSpace()
      title = "New workspace"  
      form.submit.label.text = "Create"
   
   form.name.data = workspace.name
   form.description.data = workspace.description
   form.location.data = workspace.location
   form.status.data = workspace.status
   action = url_for('.update_workspace',id=workspace.id)
   back_to = session.get('back_to', None)
   return render_template('edit_workspace.html', title=title, action=action, form=form, workspace=workspace, back_to=back_to)

@bp.route('/workspace/add', methods=['POST'], defaults={'id':None})
@bp.route('/workspace/<id>/update', methods=['POST'])
@login_required
def update_workspace(id):
   if not current_user.is_manager():
      abort(403)

   form = WorkspaceEditForm()      
   if id:
      workspace = WorkSpace.query.get_or_404(id)
      title = "Edit workspace"
      form.submit.label.text = "Update"
   else:
      workspace = WorkSpace()
      title = "New workspace"
      form.submit.label.text = "Create"

   
   if form.validate_on_submit():      
      workspace.name = form.name.data
      workspace.description = form.description.data
      workspace.location = form.location.data
      workspace.status = form.status.data

      if not workspace.id:
         db.session.add(workspace)
      db.session.commit()

      # Handle Thumbnail files 
      thumbnail = form.thumbnail.data         
      if thumbnail and thumbnail.filename != '':
         file_ext = os.path.splitext(thumbnail.filename)[1]            
         workspace.thumbnail = f"workspace_{workspace.id}{file_ext}"
         thumbnail.save(os.path.join(current_app.static_folder, 'thumbnails', workspace.thumbnail))            
         db.session.commit() # save thumbnail name
    
      flash('Your changes have been saved.')
      return redirect(url_for('.show_workspace', id=workspace.id))
   return render_template('edit_workspace.html', title=title, form=form, workspace=workspace)

@bp.route('/workspace/<id>/delete', methods=['POST'])
@login_required
def delete_workspace(id):
   if not current_user.is_manager():
      abort(403)

   workspace = WorkSpace.query.get_or_404(id)
   db.session.delete(workspace)
   db.session.commit()
   flash("Workspace has been deleted")
   return redirect(url_for('.workspaces'))

#
#  Add/Remove Required Skills
#
@bp.route('/workspace/<id>/edit_skills')
@login_required
def edit_workspace_skills(id):
  if not current_user.is_manager():
    abort(403)

  workspace = WorkSpace.query.get_or_404(id)
  all_skills = Skill.query.all()

  return render_template('workspace_edit_skills.html', title=f'Required Skills for {workspace.name}', workspace=workspace, all_skills=all_skills)

@bp.route('/workspace/<id>/add_skill/<skill_id>', methods=['POST'])
@login_required
def add_workspace_skill(id, skill_id):
  if not current_user.is_manager():
    abort(403)

  workspace = WorkSpace.query.get_or_404(id)
  skill = Skill.query.get_or_404(skill_id)
  if not workspace.requires_skill(skill):
    workspace.required_skills.append(skill)
    db.session.commit()
  
  return redirect(url_for('.edit_workspace_skills', id = workspace.id))       

@bp.route('/workspace/<id>/remove_skill/<skill_id>', methods=['POST'])
@login_required
def remove_workspace_skill(id, skill_id):
  if not current_user.is_manager():
    abort(403)

  workspace = WorkSpace.query.get_or_404(id)
  skill = Skill.query.get_or_404(skill_id)
  if workspace.requires_skill(skill):
    workspace.required_skills.remove(skill)
    db.session.commit()
  
  return redirect(url_for('.edit_workspace_skills', id = workspace.id))      