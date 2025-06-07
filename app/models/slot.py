
from app.models import db
from datetime import datetime



class Slot(db.Model):

  duration_choices = [5 * x for x in range(3, 25)]  # create list of numbers from 15 mins to 240(3 hours) going up by 5

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
    return f"<Slot {self.id}: {self.workspace_id} - {self.start_time}>"

  def status_str(self):
    if self.user_id:
      return "Booked"
    return "Available"
  
  def is_booked(self):
    if self.user_id:
      return True
    return False
  
  def is_avaliable(self):
    return(not self.is_booked())
