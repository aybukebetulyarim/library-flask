from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/turkai/Desktop/library/librarydatabase.db'

db = SQLAlchemy(app) 

class Admin(db.Model):
    __tablename__ = "admin"
    admin_id      = db.Column(db.Integer, primary_key=True)
    adminName     = db.Column(db.String, unique=True)
    adminSurname  = db.Column(db.String)
    adminUsername = db.Column (db.String)
    adminEmail    = db.Column(db.String)
    adminPass     = db.Column(db.String)

    def __init__(self, adminName:str,adminSurname:str,adminUsername:str,adminEmail:str,adminPass:str):
        self.adminName     = adminName
        self.adminSurname  = adminSurname
        self.adminUsername = adminUsername
        self.adminEmail    = adminEmail
        self.adminPass     = adminPass

class User(db.Model):
    __tablename__ = "user"
    user_id       = db.Column(db.Integer, primary_key=True)
    userName      = db.Column(db.String, unique=True)
    userSurname   = db.Column(db.String)
    username2     = db.Column(db.String)
    email         = db.Column(db.String)
    userPass      = db.Column(db.String)

    def __init__(self, userName:str, userSurname:str, username2:str, email:str, userPass:str):
        self.userName    = userName
        self.userSurname = userSurname
        self.username2   = username2
        self.email       = email
        self.userPass    = userPass

db.create_all()