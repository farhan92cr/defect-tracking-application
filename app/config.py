import os

#class Config:
 #   SECRET_KEY = os.urandom(24).hex()
  #  MONGO_URI = 'mongodb://localhost:27017/production_defects_db'

class Config:
    SECRET_KEY = 'your_secret_key'
    MONGO_URI = 'mongodb://localhost:27017/production_defects_db'
