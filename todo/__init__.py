import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager


load_dotenv()
db_key = os.getenv("DB_KEY")
db_user = os.getenv("DB_USER")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://{db_user}:{db_key}@localhost/todo_app"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from . import models, routes

db.create_all()