from flask import render_template, flash, redirect, url_for, request, abort, session

from flask_login import current_user, login_required #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import db, Slot #, WorkSpace
from app.main import bp
import datetime
from sqlalchemy import and_
from  .slot_forms import SlotBookingForm #,SlotEditForm


@bp.route('/booking/<id>/book',methods=['POST','GET'])
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
         if current_user.is_staff():
            slot.approved = 1
            slot.approved_by_id = current_user.id
         db.session.commit()      
      return redirect(session['back_to'] or url_for('.home'))
   return render_template('edit_booking.html', form=form, slot=slot)

@bp.route('/booking/<id>/unbook',methods=['POST'])
@login_required
def unbook(id):
   slot = Slot.query.get_or_404(id)  

   if slot.is_booked() and slot.user_id != current_user.id:
      abort(403) 
   
   slot.user_id = None
   slot.description = ""
   slot.approved = 0
   slot.approved_by_id = None
   db.session.commit()
   return redirect(session['back_to'] or url_for('.show_workspace', id=slot.workspace_id, date=slot.start_time.date()))


@bp.route('/booking/<id>/approve',methods=['POST'])
@login_required
def approve_slot(id):
   if not current_user.is_manager():
      abort(403)

   slot = Slot.query.get_or_404(id)  

   if slot.is_booked():
      slot.approved = 1
      slot.approved_by_id = current_user.id
      db.session.commit()
   
   return redirect(session['back_to'] or url_for('.home'))

@bp.route('/bookings/unapproved')
@login_required
def unapproved_bookings():
   if not current_user.is_manager():
      abort(403)

   today = datetime.date.today()
   slots = Slot.query.filter(and_(Slot.start_time >= today, Slot.user_id > 0, Slot.approved == 0))
   return render_template('approve_slots.html',slots=slots)

