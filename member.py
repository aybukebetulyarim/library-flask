from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/turkai/Desktop/library/database.db'

db = SQLAlchemy(app) 


class Member(db.Model):
    __tablename__ = "member"
    member_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    memberName    = db.Column(db.String, unique=True)
    memberSurname = db.Column(db.String)
    memberNick    = db.Column(db.String)
    email         = db.Column(db.String)
    memberPass    = db.Column(db.String)
    memberAuth    = db.Column(db.String)

    def __init__(self, memberName:str, memberSurname:str, memberNick:str, email:str, memberPass:str, memberAuth:str):
        self.memberName    = memberName
        self.memberSurname = memberSurname
        self.memberNick    = memberNick
        self.email         = email
        self.memberPass    = memberPass
        self.memberAuth    = memberAuth

db.create_all()