from flask import render_template, flash, redirect, url_for, request, abort, session

from flask_login import current_user, login_required 
from app.models import db, Slot, WorkSpace
from app.main import bp
import datetime
from sqlalchemy import and_
from  .slot_forms import SlotBookingForm 


@bp.route('/booking/<id>/book',methods=['POST','GET'])
@login_required
def booking(id):
   slot = Slot.query.get_or_404(id)  

   if slot.is_booked() and slot.user_id != current_user.id and not current_user.is_manager():
      abort(403) 

   form = SlotBookingForm()
   if not slot.user_id:
      form.submit.label.text = "Make Booking"  # change button if slot is not currently booked

   if request.method == 'GET':
      form.description.data = slot.description        
      return render_template('edit_booking.html', form=form, slot=slot)
   
   elif request.method == 'POST' and form.validate_on_submit():
      if form.submit.data:         
         slot.description = form.description.data         
         if not slot.user_id:
            slot.user_id = current_user.id

            if current_user.is_staff():
               slot.approved = Slot.APPROVAL["approved"]
               slot.approved_by_id = current_user.id

         if slot.approved == Slot.APPROVAL["rejected"]:
            slot.approved = Slot.APPROVAL["pending"]
            
         db.session.commit()            
         flash('Booking has been saved')
      return redirect(session['back_to'] or url_for('.home'))
   return render_template('edit_booking.html', form=form, slot=slot)

@bp.route('/booking/<id>/unbook',methods=['POST'])
@login_required
def unbook(id):
   slot = Slot.query.get_or_404(id)  

   if slot.is_booked() and slot.user_id != current_user.id and not current_user.is_manager():
      abort(403) 
   
   slot.user_id = None
   slot.description = ""
   slot.approved = 0
   slot.approved_by_id = None
   db.session.commit()
   flash('Booking has been cancelled')
   return redirect(session['back_to'] or url_for('.show_workspace', id=slot.workspace_id, date=slot.start_time.date()))


@bp.route('/booking/<id>/approve',methods=['POST'])
@login_required
def approve_booking(id):
   if not current_user.is_manager():
      abort(403)

   slot = Slot.query.get_or_404(id)  

   if slot.is_booked():
      slot.approved = Slot.APPROVAL["approved"]
      slot.approved_by_id = current_user.id
      db.session.commit()
      flash("Booking approved", "success")
   
   return redirect(session['back_to'] or url_for('.home'))

@bp.route('/booking/<id>/reject',methods=['POST'])
@login_required
def reject_booking(id):
   if not current_user.is_manager():
      abort(403)

   slot = Slot.query.get_or_404(id)  

   if slot.is_booked():
      slot.approved = Slot.APPROVAL["rejected"]
      slot.approved_by_id = current_user.id
      db.session.commit()
      flash("Booking rejected", "warning")
   
   return redirect(session['back_to'] or url_for('.home'))

@bp.route('/bookings/unapproved')
@login_required
def unapproved_bookings():
   if not current_user.is_manager():
      abort(403)

   workspaces = WorkSpace.query.order_by('name').all()  

   # remove bookings that have already been approved
   spaces = []
   for workspace in workspaces:
      #workspace.bookings = workspace.bookings.filter_by(approved=0)
      #if workspace.bookings.first(): # Only include if has atleast one booking
      #   spaces.append(workspace)
      if workspace.unapproved_bookings().first(): # has atleast one
         spaces.append(workspace)
      
   #today = datetime.date.today()
   #slots = Slot.query.filter(and_(Slot.start_time >= today, Slot.user_id > 0, Slot.approved == 0))
   session['back_to'] = url_for('.unapproved_bookings')
   return render_template('bookings_approve.html', workspaces=spaces)

