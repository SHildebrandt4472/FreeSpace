from flask import render_template, flash, redirect, url_for, request, abort, session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, Slot, WorkSpace
from app.main import bp
import datetime
#from sqlalchemy import text
from .slot_forms import SlotEditForm, SlotBookingForm

@bp.route('/slot/<id>') 
@login_required
def show_slot(id):
   slot = Slot.query.get_or_404(id)
   return render_template('show_slot.html',slot = slot)


@bp.route('/workspace/<workspace_id>/new_slot/<datetime:start_time>')
@login_required
def new_slot(workspace_id, start_time):
   if not current_user.is_admin():
      abort(403)
   
   title = "New booking slot"
   workspace = WorkSpace.query.get_or_404(workspace_id)
   
   slot = Slot()
   slot.start_time = start_time  

   form = SlotEditForm()
   form.start_time.data = slot.start_time
   form.duration.data = slot.duration
   form.description.data = slot.description
   form.repeating.data = slot.repeating
   action = url_for('.add_slot', workspace_id=workspace.id)
   return render_template('edit_slot.html', title=title, action=action, form=form)


@bp.route('/workspace/<workspace_id>/add_slot',methods=['POST'])
@login_required
def add_slot(workspace_id):
   if not current_user.is_admin():
      abort(403)
   
   workspace = WorkSpace.query.get_or_404(workspace_id)
   title = "New booking slot"
   slot = Slot()

   form = SlotEditForm()
   if form.validate_on_submit():
        slot.start_time = form.start_time.data
        slot.duration = form.duration.data
        slot.description = form.description.data
        slot.repeating = form.repeating.data
        
        workspace.slots.append(slot)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.show_workspace', id=workspace.id))
   return render_template('new_slot.html', title=title, form=form)

@bp.route('/slot/<id>/book',methods=['POST','GET'])
@login_required
def booking(id):
   slot = Slot.query.get_or_404(id)  

   if slot.is_booked() and slot.user_id != current_user.id:
      abort(403) 

   form = SlotBookingForm()
   if request.method == 'GET':
      form.description.data = slot.description  
      return render_template('edit_booking.html', form=form, slot=slot)
   elif request.method == 'POST' and form.validate_on_submit():
      if form.submit.data:
         slot.user_id = current_user.id
         slot.description = form.description.data
         db.session.commit()      
      return redirect(session['back_to'] or url_for('.home'))
   return render_template('edit_booking.html', form=form, slot=slot)

@bp.route('/slot/<id>/unbook',methods=['POST'])
@login_required
def unbook(id):
   slot = Slot.query.get_or_404(id)  

   if slot.is_booked() and slot.user_id != current_user.id:
      abort(403) 
   
   slot.user_id = None
   db.session.commit()
   return redirect(url_for('.show_workspace', id=slot.workspace_id, date=slot.start_time.date()))


@bp.route('/slot/<id>/edit')
@login_required
def edit_slot(id):
   if not current_user.is_admin():
      abort(403)  

   title = "Edit booking slot"   
   slot = Slot.query.get_or_404(id)   

   form = SlotEditForm()
   form.start_time.data = slot.start_time
   form.duration.data = slot.duration
   form.description.data = slot.description
   form.repeating.data = slot.repeating
   action = url_for('.update_slot', id=slot.id)
   return render_template('edit_slot.html', title=title, form=form, action=action,)


@bp.route('/slot/<id>/update', methods=['POST'])
@login_required
def update_slot(id):
   if not current_user.is_admin():
      abort(403)
     
   slot = Slot.query.get_or_404(id)   
   
   form = SlotEditForm()
   if form.validate_on_submit():
        slot.start_time = form.start_time.data
        slot.duration = form.duration.data
        slot.description = form.description.data
        slot.repeating = form.repeating.data   
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.show_workspace', id=slot.workspace.id))

   title = "Edit booking slot" 
   action = url_for('.update_slot', id=slot.id)
   return render_template('edit_slot.html', title=title, form=form, action=action)