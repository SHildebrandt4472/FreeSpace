import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object): #This is the main configurations for the app
  DATABASE_FILENAME = "freespace.db"
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', DATABASE_FILENAME) 
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = "ThisIsMySuperSecretKey"  

  