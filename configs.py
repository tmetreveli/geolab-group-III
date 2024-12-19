from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["SECRET_KEY"] = "asdfgsdrge434twerfgaer"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"