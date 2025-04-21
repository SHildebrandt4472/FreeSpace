
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from datetime import datetime

login = LoginManager()

ACCESS = {
  'student'    : 10,
  'staff'      : 20,
  'manager'    : 30,
  'admin'      : 40,
}

ACCESS_STRS = {
  ACCESS['student']   : "Student",
  ACCESS['staff']     : "Staff",
  ACCESS['manager']   : "Manager",
  ACCESS['admin']     : "Admin",
}

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(32), index=True, unique=True)
  display_name = db.Column(db.String(32))  
  access = db.Column(db.Integer, default=ACCESS['student'])

  email = db.Column(db.String(120), index=True, unique=True)
  email_verified = db.Column(db.Integer)
  password_hash = db.Column(db.String(128))
  last_seen = db.Column(db.DateTime) 
  created_at = db.Column(db.DateTime, default=db.func.datetime('now')) 
  last_modified = db.Column(db.DateTime, default=db.func.datetime('now'), onupdate=db.func.datetime('now')) 

  def __repr__(self):
    return f"<User {self.id}: {self.username}>"

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    if not self.password_hash:
      return False
    return check_password_hash(self.password_hash, password)

  def is_student(self):
    return self.access >= ACCESS['student']

  def is_admin(self):
    return self.access >= ACCESS['admin']
  
  def name(self):
    return self.display_name or self.username

  def access_str(self):
    if self.access in ACCESS_STRS:
      return ACCESS_STRS[self.access]
    return "Unknown"

  def update_last_seen(self):
    last_seen = self.last_seen if self.last_seen else datetime.fromtimestamp(0)
    if (datetime.now() - last_seen).total_seconds() > 600:  # More than 10 minutes ago     
      self.last_seen = datetime.now()
      db.session.commit()

@login.user_loader
def load_user(id):
  return User.query.get(int(id))


