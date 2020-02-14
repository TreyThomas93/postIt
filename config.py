import os
from models import Users, Posts

SECRET_KEY = os.urandom(24)

## SQLALCHEMY CONFIG ##
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.getcwd()}/postIt.db"
SQLALCHEMY_BINDS = ({"Posts" : f"sqlite:///{os.getcwd()}/postIt.db"})

## FLASK MAIL CONFIG ##
MAIL_SERVER = "smtp.googlemail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("GMAIL_USERNAME") # use your own email address here
MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") # use your own email password here