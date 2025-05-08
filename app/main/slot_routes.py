from flask import render_template, flash, redirect, url_for, request, abort #,session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, Slot, WorkSpace
from app.main import bp
import datetime
#from sqlalchemy import text
from .slot_forms import SlotEditForm

@bp.route('/slot/<id>') 
@login_required
def show_slot(id):
   slot = Slot.query.get_or_404(id)

   return render_template('show_slot.html',slot = slot)

@bp.route('/workspace/<workspace_id>/new_slot', defaults={'slot_id':None})
@bp.route('/slot/<slot_id>/edit', defaults={'workspace_id':None})
@login_required
def edit_slot(slot_id,workspace_id):

   if not current_user.is_admin():
      abort(403)

   if workspace_id:
      workspace = WorkSpace.query.get_or_404(workspace_id)
      title = "New booking slot"
      slot = Slot()
      slot.start_time = datetime.datetime.now()

   elif slot_id:
      slot = Slot.query.get_or_404(slot_id)
      workspace = Slot.workspace
      title = "Edit booking slot"
   
   else:
      abort(403)

   form = SlotEditForm()
   form.start_time.data = slot.start_time
   form.duration.data = slot.duration
   form.description.data = slot.description
   form.repeating.data = slot.repeating
   action = url_for('.update_slot',slot_id=slot_id,workspace_id=workspace_id)
   return render_template('edit_slot.html', title=title, action=action, form=form)

@bp.route('/workspace/<workspace_id>/add_slot',methods=['POST'], defaults={'slot_id':None})
@bp.route('/slot/<slot_id>/update', methods=['POST'], defaults={'workspace_id':None})
@login_required
def update_slot(workspace_id, slot_id):
   if not current_user.is_admin():
      abort(403)

   if workspace_id:
      workspace = WorkSpace.query.get_or_404(workspace_id)
      title = "New booking slot"
      slot = Slot()

   elif slot_id:
      slot = Slot.query.get_or_404(slot_id)
      workspace = Slot.workspace
      title = "Edit booking slot"
   
   else:
      abort(403)

   form = SlotEditForm()
   
   print(form.start_time)

   if form.validate_on_submit():
        slot.start_time = form.start_time.data
        slot.duration = form.duration.data
        slot.description = form.description.data
        slot.repeating = form.repeating.data

        if not slot.id:
            workspace.slots.append(slot)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.show_workspace', id=workspace.id))
   return render_template('edit_slot.html', title=title, form=form)