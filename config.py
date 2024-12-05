import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost/personal_finance_tracker"
    SQLALCHEMY_TRACK_MODIFICATIONS = False