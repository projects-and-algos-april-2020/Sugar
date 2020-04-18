from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key = "WHITNEY IS SO BEAUTIFUL"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sugar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from models import Users
