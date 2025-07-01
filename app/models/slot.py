
from app.models import db
from datetime import datetime, timedelta
from sqlalchemy import and_
import datetime



class Slot(db.Model):

  duration_choices = [5 * x for x in range(3, 25)]  # create list of numbers from 15 mins to 240(3 hours) going up by 5
  hour_choices = [x for x in range(7, 19)] 
  minute_choices = [(x, f"{x:02d}") for x in range(0, 60, 5)] 

  id = db.Column(db.Integer, primary_key=True)
  workspace_id = db.Column(db.Integer, db.ForeignKey('work_space.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  start_time = db.Column(db.DateTime)
  duration = db.Column(db.Integer, default=30)

  description = db.Column(db.Text)
  repeating = db.Column(db.Integer, default=1)  # 1 = repeat, 0 - not repeat

  approved = db.Column(db.Integer, default=0)  # 1 = approved, 0 - not approved
  approved_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


  created_at = db.Column(db.DateTime, default=db.func.datetime('now')) 
  last_modified = db.Column(db.DateTime, default=db.func.datetime('now'), onupdate=db.func.datetime('now')) 

  def __repr__(self):
    return f"<Slot {self.id}: {self.workspace_id} - {self.start_time.strftime('%a %d %b %H:%M')} ({self.duration} mins)>"

  def booking_status_str(self, current_user=None):
    if current_user and self.user_id == current_user.id:
      return "Booked"    
    if self.user_id:
      return "Unavailable"
    return "Available"
  
  def status_str(self):
    if self.repeating: 
      return "Weekly"        
    return "Onceoff"

  
  def is_booked(self):
    if self.user_id:
      return True
    return False
  
  def is_available(self):
    return(not self.is_booked())
  
  # check to see this time slot clashes (overlaps) any existing time slot
  def has_a_clash(self):    
    search_start = self.start_time - timedelta(hours=12)  # 12 hours before this time slot
    search_end = self.start_time + timedelta(minutes=(self.duration-1)) # end of this time slot
    # search DB for a possible clash/overlapping times
    slot = Slot.query.filter(and_(Slot.start_time.between(search_start, search_end),  # start time with a range that COULD overlap
                                  Slot.workspace_id == self.workspace_id,             # Has same worspace id
                                  Slot.id != self.id                                  # isn't THIS slot (could be if modifying an existing slot) 
                                  )).order_by(
                                    Slot.start_time.desc()                            # order by starttime descending (so first item found is best possible clash) 
                                  ).first()     # only return 1 record
                            
    #print(f"Found Slot: {slot}")    
    if slot:  # found atleast one slot that COULD overlap
      end_time = slot.start_time + timedelta(minutes=slot.duration)
      if end_time > self.start_time:  # CLASH
        #print(f"Clash: {self} with {slot}")
        #print(f"end_time: {end_time}  start_time: {self.start_time}")
        return True   # It DOES have a Clash
      
      
    return False  # No Clash Found
  
  def copy_to(self, workspace_id=None, day=None):

    if not workspace_id and not day:  # must pass atleast one
      return False

    if not workspace_id:
      workspace_id = self.workspace_id  # Same Workspace

    if not day:
      day = self.start_time.date()  # Same day

    new_slot = Slot(workspace_id = workspace_id,
                    start_time = datetime.datetime.combine(day, self.start_time.time()),
                    duration = self.duration,
                    repeating = self.repeating)
    
    if new_slot.has_a_clash():  # Clashes with another time slot (for same workspace)
      return False
    
    # otherwsie add the new_slot
    db.session.add(new_slot)
    db.session.commit()
    return True  
  