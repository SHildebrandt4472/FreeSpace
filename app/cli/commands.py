
#
#  Command Line Interface
#
#  These functions can be accessed from command line as follows....
#
#    flask cli COMMAND [ARGS]
#
#  A list of avaiable commands can be generated with ...
#
#    flask cli
#
#
#import click
from app.models import db, User, WorkSpace, Slot
from app.cli import bp
import datetime

@bp.cli.command("init_data")
def init_data():  # Preset data for testing and initial deployment 
  """Add initial dbug data to db"""

  User.query.delete()  
  
  user = User(username="sam",  # Creating a new user with differents attributes
              email="sam@fullsteam.net",
              display_name="Sam",
              access=40)              
  user.set_password("train")
  db.session.add(user)  
  db.session.commit()
  print("Created:", user)  

  user = User(username="demo",  # Creating a new demo user with differents attributes
           email="demo@demo.com",
           display_name="Demo User")             
  user.set_password("demo")
  db.session.add(user)  
  db.session.commit()
  print("Created:", user)    

  
  WorkSpace.query.delete()

  laser_cutter = WorkSpace(name="Laser cutter 1", 
                          description="The good one",
                          location="Machiene room 1")
  db.session.add(laser_cutter)
  db.session.commit()
  print("Created:", laser_cutter)

  printer = WorkSpace(name="3d printer 1", 
                          description="The not so good one",
                          location="Machiene room 1")
  db.session.add(printer)
  db.session.commit()
  print("Created:", printer)
    
  
  Slot.query.delete()

  for i in range(10):
    
    today = datetime.date.today()
    MyTime = datetime.time(8, 0, 0)
    DateTime = datetime.datetime.combine(today, MyTime)  
    slot = Slot(workspace_id=laser_cutter.id,
                start_time=DateTime + datetime.timedelta(minutes=i*30),
                description=f"Slot {i}")
    db.session.add(slot)
    db.session.commit()
    print("Created:", slot)
@bp.cli.command("make_css")
def make_css():
  min = 0
  for h in range(7,20): 
    for m in range(0,60,5):
      print(f".time_{h:02}-{m:02} {{ top: calc({min} * var(--px_per_min)); }}")
      min+= 5
