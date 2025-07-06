
#
#  Setup a Demo database from command line#
#
#    flask cli init_demo
#
#
from flask import current_app
from app.models import db, User, WorkSpace, Slot, Skill, user_skill_table, workspace_skill_table
from app.cli import bp
import datetime as dt
import os
import shutil

users = {
  'sam':      {'display_name':'Sam Hildebrandt',     'email':'sam@fullsteam.net',     'access': 40, 'skills':['onguard','3dprint','laser','woodwork'] },
  'homer':    {'display_name':'Homer Simpson',       'email':'homer@simpsons.com',    'access': 30, 'skills':['onguard','3dprint','laser','woodwork','staff'] },  
  'edna':     {'display_name':'Edna Crabappel',      'email':'edna@simpsons.com',     'access': 20, 'skills':['onguard','3dprint','laser','woodwork','staff'] },  
  'bart':     {'display_name':'Bart Simpson',        'email':'bart@simpsons.com',     'access': 10, 'skills':[]},  
  'lisa':     {'display_name':'Lisa Simpson',        'email':'lisa@simpsons.com',     'access': 10, 'skills':['onguard','woodwork','3dprint','laser'] },  
  'milhouse': {'display_name':'Milhouse Van Houton', 'email':'milhouse@simpsons.com', 'access': 10, 'skills':['onguard','3dprint'] },  
  'ferb':     {'display_name':'Ferb Fletcher',       'email':'ferb@danvil.com',       'access': 10, 'skills':['onguard','3dprint', 'laser'] },  
  'phineas':  {'display_name':'Phineas Flynn',       'email':'phineas@danvil.com',    'access': 10, 'skills':['onguard','3dprint', 'laser'] },  
  'candice':  {'display_name':'Candice Flynn',       'email':'candice@danvil.com',    'access': 10, 'skills':['onguard','woodwork'] },   
  'ralph':    {'display_name':'Ralph Wiggum',        'email':'ralph@simpsons.com',    'access': 10, 'skills':['onguard','woodwork'] },   
}

skills = {   
   'onguard':  {'description': 'OnGuard Safety Certificate'},       
   '3dprint':  {'description': '3D Printer Badge'}, 
   'laser':    {'description': 'Laser Cutter Badge'}, 
   'woodwork': {'description': 'General Woodworking Tools Badge'},
   'ptools':   {'description': 'Woodworking PowerTools Badge'},
   'staff':    {'description': 'Staff Member'},     
}


weekday_slots_1 = [
   {'start': dt.time(7,15), 'duration':75},
   {'start': dt.time(13,00), 'duration':30},
   {'start': dt.time(15,30), 'duration':120},
   {'start': dt.time(17,30), 'duration':120},      
]

workspaces = {
  'LASER-01':   {'description':'Laser Cutter',   'location': 'Machine Room 1',   'skills': ['onguard','laser'],   'thumbnail':'laser.png'},
  '3DPRINT-01': {'description':'3D Printer 1',   'location': 'Tech Room 1',      'skills': ['onguard','3dprint'], 'thumbnail':'3dprinter.png'},
  '3DPRINT-02': {'description':'3D Printer 2',   'location': 'Tech Room 1',      'skills': ['onguard','3dprint'], 'thumbnail':'3dprinter.png'},
  '3DPRINT-03': {'description':'3D Printer 3',   'location': 'Tech Room 1',      'skills': ['onguard','staff'],   'thumbnail':'3dprinter2.png'},  
  'BENCH-01':   {'description':'B1 Wood Tech Bench','location': 'Timber Room',   'skills': ['onguard','woodwork'],'thumbnail':'workbench.png'},
  'BENCH-02':   {'description':'B2 Wood Tech Bench','location': 'Timber Room',   'skills': ['onguard','woodwork'],'thumbnail':'workbench.png'},    
  'BENCH-03':   {'description':'B3 Wood Tech Bench','location': 'Timber Room',   'skills': ['onguard','woodwork'],'thumbnail':'workbench.png'},    
  'BENCH-04':   {'description':'B4 Wood Tech Bench','location': 'Timber Room',   'skills': ['onguard','woodwork'],'thumbnail':'workbench.png'},      
  'BSAW-01':    {'description':'Band Saw',          'location': 'Machine Room 2','skills': ['onguard','woodwork', 'ptools'],'thumbnail':'bandsaw.png'},      
  'CSAW-01':    {'description':'Circular Saw',      'location': 'Machine Room 2','skills': ['onguard','woodwork', 'ptools'],'thumbnail':'sawbench.png'},      
}

weekday_slots_1 = [
   {'start': dt.time(7,15), 'duration':75},
   {'start': dt.time(13,00), 'duration':30},
   {'start': dt.time(15,30), 'duration':120},
   {'start': dt.time(17,30), 'duration':120},      
]

weekend_slots_1 = [
   {'start': dt.time(10,00), 'duration':60},
   {'start': dt.time(11,00), 'duration':60},
   {'start': dt.time(12,00), 'duration':60},
   {'start': dt.time(13,00), 'duration':60},      
   {'start': dt.time(14,00), 'duration':60},      
]

lunch_slots_1 = [
   {'start': dt.time(13,00), 'duration':30},
]

slots = {      # Monday,          Tuesday,         Wednesday,       Thursday,        Friday,         Saturday,         Sunday
  'LASER-01':   [weekday_slots_1, None,            weekday_slots_1, weekday_slots_1, weekday_slots_1, None,            None],
  '3DPRINT-01': [weekday_slots_1, weekday_slots_1, weekday_slots_1, weekday_slots_1, weekday_slots_1, weekend_slots_1, None],
  '3DPRINT-02': [weekday_slots_1, weekday_slots_1, weekday_slots_1, weekday_slots_1, weekday_slots_1, weekend_slots_1, None],
  '3DPRINT-03': [weekday_slots_1, weekday_slots_1, weekday_slots_1, weekday_slots_1, weekday_slots_1, weekend_slots_1, None],
  'BENCH-01':   [weekday_slots_1, weekday_slots_1, None,            None,            None,            None,            None],
  'BENCH-02':   [weekday_slots_1, weekday_slots_1, None,            None,            None,            None,            None],
  'BENCH-03':   [weekday_slots_1, weekday_slots_1, None,            None,            None,            None,            None],
  'BENCH-04':   [weekday_slots_1, weekday_slots_1, None,            None,            None,            None,            None],
  'BSAW-01':    [lunch_slots_1,   lunch_slots_1,   lunch_slots_1,   lunch_slots_1,   lunch_slots_1,   None,            None],
  'CSAW-01':    [lunch_slots_1,   lunch_slots_1,   lunch_slots_1,   lunch_slots_1,   lunch_slots_1,   None,            None],
}

def add_slots_to(workspace, day, slot_times):
   for time in slot_times:
      slot = Slot(start_time = dt.datetime.combine(day, time['start']),
                  duration = time['duration'])          
      workspace.slots.append(slot)
      db.session.commit()
      print("  Add booking slot: ", slot)

@bp.cli.command("init_demo")
def init_demo():  # Preset data for Demo 

  User.query.delete()  
  WorkSpace.query.delete()
  Slot.query.delete()
  Skill.query.delete()  
  db.session.query(user_skill_table).delete()
  db.session.query(workspace_skill_table).delete()
  db.session.commit()  

  # Delete OLD thumbnail files
  thumbnails_path = os.path.join(current_app.static_folder, 'thumbnails')      
  for filename in os.listdir(thumbnails_path):
    file_path = os.path.join(thumbnails_path, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")     

  # create skills
  for s in skills:
    skill = Skill(description=skills[s]['description'])   
    skills[s]['skill']=skill
    db.session.add(skill)
    db.session.commit()
    print("Created:", skill)        
  
  # Create Users  
  for username in users:    
    details = users[username]

    user = User(username=username,
                display_name=details['display_name'],
                email=details['email'],
                access=details['access'])
    details['user']=user # store for future use
    user.set_password(username)  # use username as password     
    db.session.add(user)  
    db.session.commit()        
    print("Created:", user)  

    # Add Skills 
    for sk in details['skills']:      
      skill = skills[sk]['skill']
      user.skills.append(skills[sk]['skill'])  # add skills
      db.session.commit()
      print("  Added Skill: ", skills[sk]['skill'])     

  # create Workspaces
  for name in workspaces:
    details = workspaces[name]

    workspace = WorkSpace(name=name,
                          description=details['description'],
                          location=details['location'])  
    details['workspace']=workspace # store for future use
    db.session.add(workspace)
    db.session.commit()
    print("Created:", workspace)

    # add thumbnails
    if 'thumbnail' in details:
      filename = details['thumbnail']     

      file_ext = os.path.splitext(filename)[1]            
      thumbnail_file = f"workspace_{workspace.id}{file_ext}"
      src_filename = os.path.join(current_app.root_path, '..', 'demo_thumbnails', filename)            
      dest_filename = os.path.join(current_app.static_folder, 'thumbnails', thumbnail_file)      
      shutil.copy(src_filename, dest_filename)         
      workspace.thumbnail = thumbnail_file
      db.session.commit()
      print("  Added Thumbnail:", thumbnail_file)          
     
    # Add Skills 
    for sk in details['skills']:      
      skill = skills[sk]['skill']
      workspace.required_skills.append(skills[sk]['skill'])  # add skills
      db.session.commit()
      print("  Added Required Skill: ", skills[sk]['skill'])         


    # Add Booking Slots   
    today = dt.date.today()
    monday_lastweek = today - dt.timedelta(days=today.weekday())               

    if name in slots:
      for i in range(7):                  
         if i < len(slots[name]):
            day = monday_lastweek + dt.timedelta(days=i)              
            times = slots[name][i]
            if times:
              add_slots_to(workspace, day, times)  

  # Copy ALL slots for all wookspaces to future weeks
  for slot in Slot.query.all():        
    for weeks in range(1,3):
      to_date = slot.start_time.date() + dt.timedelta(weeks=weeks)
      slot.copy_to(day=to_date)

  # Make bookings
  usernames = list(users.keys())  
  usernames += usernames[1:] + usernames[2:] + usernames[:3] + usernames[:4]
  usernames *= 3

  usr = 0  
  for slot in Slot.query.filter(Slot.start_time >= today).order_by(Slot.start_time).all():
    if usr%3 != 0: # skip 3rd slot
      user = users[usernames[usr]]['user']  
      if user.has_skills_for(slot.workspace):
        slot.user_id = user.id
        slot.description = "Do Something"
        if usr%3 == 0 or user.access > 10:        
          slot.approved = 1
          slot.approved_by_id = users['homer']['user'].id

    usr += 1
    if usr >= len(usernames):
      break     

#
#  Special Cases
#
  workspace = workspaces['CSAW-01']['workspace']
  workspace.status = WorkSpace.STS_OUT_SERVICE
  db.session.commit()