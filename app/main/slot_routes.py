from flask import render_template, flash, redirect, url_for, request, abort, session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, Slot, WorkSpace
from app.main import bp
from datetime import date, timedelta
from sqlalchemy import and_
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
   
   title = "New Booking Slot"
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



@bp.route('/slots/weekly')
@login_required
def weekly_slots():
   if not current_user.is_admin():
      abort(403)

   start_week = -2       # means 2 weeks ago
   number_of_weeks = 10  # number of weeks to display
   
   today = date.today()
   this_monday = today - timedelta(days = today.weekday())   # today minus the weekday
   week_start_dates = []  # list of week start dates
   weeks = []
   for w in range(start_week, start_week + number_of_weeks):                                   
      week_start_dates.append( this_monday + timedelta(weeks=w) )  
      weeks.append(w)

   workspaces = WorkSpace.query.all()  

   weekly_slot_counts = {}

   for workspace in workspaces:   
      slot_counts = []  # list of slot counts for each week for this workspace
      for start_date in week_start_dates:
         end_date = start_date + timedelta(weeks=1)

         repeating_cnt = 0         
         for slot in workspace.slots.filter(Slot.start_time.between(start_date,end_date)):
            if slot.repeating:
               repeating_cnt += 1  # count repeating booking slots in this week
            
         slot_counts.append({'date': start_date, 'count': repeating_cnt})          

      weekly_slot_counts[workspace.id] = slot_counts            
      
   return render_template('weekly_slots.html', workspaces=workspaces, weekly_slot_counts=weekly_slot_counts, week_start_dates=week_start_dates)