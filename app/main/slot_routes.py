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


@bp.route('/slots/weekly', defaults={'start_week':-1})
@bp.route('/slots/weekly/<start_week>')
@login_required
def weekly_slots(start_week):
   if not current_user.is_admin():
      abort(403)

   start_week = int(start_week)       # means 2 weeks ago
   number_of_weeks = 10  # number of weeks to display
   
   today = date.today()
   this_monday = today - timedelta(days = today.weekday())   # today minus the weekday
   columns = []  # list of columns to be displayed

   for w in range(start_week, start_week + number_of_weeks):                                   
      columns.append({'date': this_monday + timedelta(weeks=w), 
                      'week': w,
                      'cells': {},
                      'class': 'this-week' if w == 0 else '',
                      })             
          
   workspaces = WorkSpace.query.all()

   for workspace in workspaces:     
      slot_counts = []  # list of slot counts for each week for this workspace
      for col in columns:
         start_date = col['date']
         end_date = start_date + timedelta(weeks=1)         

         repeating_cnt = 0         
         total_cnt = 0
         booked_cnt = 0
         for slot in workspace.slots.filter(Slot.start_time.between(start_date,end_date)):
            total_cnt += 1
            if slot.repeating:
               repeating_cnt += 1  # count repeating booking slots in this week            
            if slot.is_booked():
               booked_cnt += 1   
         
         if total_cnt == 0:
             class_str = 'empty'  
         elif repeating_cnt == total_cnt:
            class_str = 'repeating-only'
         else:   
            class_str = 'some-oneoffs'                   

         if booked_cnt > 0:
             class_str = 'some-booked'   

         col['cells'][workspace.id] = {'display': str(repeating_cnt) if total_cnt else '',   #Value to display
                                       'slot_cnt': total_cnt,
                                       'class': class_str,
                                      }

   # find last column with slots in it
   last_col = None
   for col in columns:         
      has_slots = False
      for cell in col['cells']:
         if col['cells'][cell]['slot_cnt'] > 0:
            has_slots = True
            break # no point continuing, found some slots
         
      if has_slots:
         last_col = col

   if last_col and last_col != columns[-1]:         
      last_col['copy_url'] = url_for('.copy_weekly_slots', from_week=last_col['week'], to_week=last_col['week']+1)

   prev_url = url_for('.weekly_slots', start_week=start_week-7)   
   next_url = url_for('.weekly_slots', start_week=start_week+7)   
      
   return render_template('weekly_slots.html', workspaces=workspaces, columns=columns, next_url=next_url, prev_url=prev_url)


@bp.route('/slots/weekly/copy/<int:from_week>/<int:to_week>',methods=['POST'])
@login_required
def copy_weekly_slots(from_week, to_week):
   if not current_user.is_admin():
      abort(403)

   today = date.today()
   this_week = today - timedelta(days = today.weekday()) # Monday of this week (today minus the weekday)
   from_start = this_week + timedelta(weeks=from_week)  # week 0 is this week
   from_end = from_start + timedelta(days=7)

   for slot in Slot.query.filter(Slot.start_time.between(from_start, from_end)):
      if slot.repeating:
         to_date = slot.start_time.date() + timedelta(weeks = (to_week - from_week))
         slot.copy_to(day=to_date)

   return redirect(url_for('.weekly_slots'))