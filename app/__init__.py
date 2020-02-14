from flask import Flask, Blueprint
from extensions import db, login_manager, mail
import os

app = Flask(__name__, template_folder=None, static_folder=None)

path_to_config = os.getcwd()

app.config.from_pyfile(f"{path_to_config}/config.py")

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

# IMPORT AND REGISTER BLUEPRINTS
from .includes import includes
from .home import home
from .auth import authorize

app.register_blueprint(includes)
app.register_blueprint(home)
app.register_blueprint(authorize)