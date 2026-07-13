import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv("")
  DEBUG = False
  TESTING = False
  
class DevelopmentConfig(Config):
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
  pass

class ProductionConfig(Config):
  pass