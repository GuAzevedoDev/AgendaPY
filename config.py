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
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = "Lax"
  SESSION_COOKIE_SECURE = True
  PERMANENT_SESSION_LIFETIME = 1800  # 30 min em segundos

class DevelopmentConfig(Config):
  DEBUG = True
  SESSION_COOKIE_SECURE = False  # dev roda em HTTP, cookie Secure nunca seria enviado

class TestingConfig(Config):
  TESTING = True
  SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
  pass