
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
from app.models import db, User, WorkSpace, Slot, Skill, user_skill_table, workspace_skill_table
from app.cli import bp
import datetime

@bp.cli.command("init_data")
def init_data():  # Preset data for testing and initial deployment 
  """Add initial dbug data to db"""

  User.query.delete()  
  
  sam = User(username="sam",  # Creating a new user with differents attributes
              email="sam@fullsteam.net",
              display_name="Sam",
              access=40)              
  sam.set_password("train")
  db.session.add(sam)  
  db.session.commit()
  print("Created:", sam)  

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

  Skill.query.delete()  

  
  db.session.query(user_skill_table).delete()
  db.session.query(workspace_skill_table).delete()
  db.session.commit()  

  skill = Skill(description="OnGuard Safety Certificate")    
  db.session.add(skill)
  db.session.commit()
  print("Created:", skill)

  sam.skills.append(skill)
  user.skills.append(skill)
  laser_cutter.required_skills.append(skill)
  db.session.commit()

  skill = Skill(description="General Woodworking Tools Badge")
  db.session.add(skill)    
  db.session.commit()
  print("Created:", skill)

  sam.skills.append(skill)
  db.session.commit()

  skill = Skill(description="3D Printer Badge")
  db.session.add(skill)
  db.session.commit()
  print("Created:", skill)

  skill = Skill(description="Laser Cutter Badge")
  laser_cutter.required_skills.append(skill)
  db.session.add(skill)
  db.session.commit()
  print("Created:", skill)

  sam.skills.append(skill)
  db.session.commit()


  skill = Skill(description="Circular Saw Badge")
  db.session.add(skill)
  db.session.commit()
  print("Created:", skill)

  print("Sam can use laser cutter:", sam.has_skills_for(laser_cutter))
  print("User can use laser cutter:", user.has_skills_for(laser_cutter))


  # print(f"Testing Clash")
  # clash = slot.has_a_clash()
  # print(f"Test Clash {slot}: {clash}\n")               

  # slot.start_time -= datetime.timedelta(minutes=45)
  # clash = slot.has_a_clash()
  # print(f"Test Clash {slot}: {clash}\n")             

  # slot.start_time -= datetime.timedelta(minutes=60)
  # slot.workspace_id = 2
  # clash = slot.has_a_clash()
  # print(f"Test Clash {slot}: {clash}\n")             

  slot.copy_to(workspace_id=printer.id)

@bp.cli.command("make_css")
def make_css():
  min = 0
  for h in range(7,20): 
    for m in range(0,60,5):
      print(f".time_{h:02}-{m:02} {{ top: calc({min} * var(--px_per_min)); }}")
      min += 5