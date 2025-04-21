
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
from app.models import db, User
from app.cli import bp
#import datetime

@bp.cli.command("init_data")
def init_data():  # Preset data for testing and initial deployment 
  """Add initial dbug data to db"""

  User.query.delete()  
  
  user = User(username="sam",  # Creating a new user with differents attributes
              email="sam@fullsteam.net",
              display_name="Sam")              
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

  

  
  
  
