
from app.models import db
from datetime import datetime
from sqlalchemy import and_
from app.models.slot import Slot

workspace_skill_table = db.Table('workspace_skill',
  db.Column('workspace_id', db.Integer, db.ForeignKey('work_space.id', ondelete='CASCADE'), primary_key=True),
  db.Column('skill_id', db.Integer, db.ForeignKey('skill.id', ondelete='CASCADE'), primary_key=True)
)

class WorkSpace(db.Model):
  STS_IN_SERVICE = 1
  STS_OUT_SERVICE = 2
  
  STS_STRINGS = {
    STS_IN_SERVICE: "In service",
    STS_OUT_SERVICE: "Out of service"
  }

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(15), index=True, unique=True)
  description = db.Column(db.Text)  

  location = db.Column(db.String(32))
  status = db.Column(db.Integer, default=STS_IN_SERVICE)

  thumbnail = db.Column(db.String(32))

  created_at = db.Column(db.DateTime, default=db.func.datetime('now')) 
  last_modified = db.Column(db.DateTime, default=db.func.datetime('now'), onupdate=db.func.datetime('now')) 
  slots = db.relationship('Slot', backref='workspace', lazy='dynamic', cascade="all, delete")
  #bookings = db.relationship('Slot', 
  #                           primaryjoin=and_(Slot.workspace_id == id, Slot.start_time > db.func.datetime('now'), Slot.user_id != None), 
  #                           lazy='dynamic')
  
  required_skills = db.relationship('Skill', secondary=workspace_skill_table, backref='workspaces')

  def __repr__(self):
    return f"<WorkSpace {self.id}: {self.name}>"
  

  def unapproved_bookings(self):
    bookings = self.slots.filter(and_(Slot.start_time > db.func.datetime('now'), Slot.user_id != None, Slot.approved == 0))
    return bookings  

  def status_str(self):
    if self.status in WorkSpace.STS_STRINGS:
      return WorkSpace.STS_STRINGS[self.status]
    return "Unknown"

  def status_choices():
    choices=[]
    for status in WorkSpace.STS_STRINGS:
      choices.append((status,WorkSpace.STS_STRINGS[status]))
    return choices
  
  def requires_skill(self, required_skill):
    for skill in self.required_skills:       
      if skill.id == required_skill.id:
        return True
    return False