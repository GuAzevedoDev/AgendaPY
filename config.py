import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.getenv("SECRET_KEY")
  DEBUG = False
  TESTING = False

  TEMPLATE_FOLDER = "views/templates"
  STATIC_FOLDER = "views/static"

  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "banco.db")

class DevelopmentConfig(Config):
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
  pass

class ProductionConfig(Config):
  pass