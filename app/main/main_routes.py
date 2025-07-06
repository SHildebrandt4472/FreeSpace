from flask import render_template, flash, redirect, url_for, request , session

from flask_login import current_user #, login_user, logout_user #, login_required
#from urllib.parse import urlparse
from app.models import Slot
from app.main import bp
import datetime
#from sqlalchemy import text


@bp.route('/')
@bp.route('/index')
def home():  # Main home page
    if not current_user.is_authenticated:
      return redirect(url_for('.login'))  # Redirect to login page if not logged in
    
    today = datetime.date.today()
    bookings = current_user.bookings.filter(Slot.start_time >= today)
    
    #previous_bookings = current_user.bookings.filter(Slot.start_time < today)
    #previous_bookings = current_user.bookings
    previous_workspaces = []
    for booking in current_user.bookings: # all bookings past and present
        if booking.workspace_id not in [ws.id for ws in previous_workspaces]:
            previous_workspaces.append(booking.workspace)

    session['back_to'] = url_for('.home')

    return render_template('index.html',bookings=bookings, previous_workspaces=previous_workspaces, page='MyBookings')

