
from app.models import db


class Skill(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(20), unique=True)

  def __repr__(self):
    return f'<Skill: {self.id}>' 
  
