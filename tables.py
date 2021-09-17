from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datab.db'

db = SQLAlchemy(app) 

class LibraryTable(db.Model):
    __tablename__= "libraryTable"
    book_id      = db.Column(db.Integer, primary_key = True)
    book_name    = db.Column(db.String)
    edition_year = db.Column(db.String)
    author       = db.Column(db.String)
    owner_name   = db.Column(db.String)
    category     = db.Column(db.String)
    translator   = db.Column(db.String)
    date_time    = db.Column(db.String)
    log          = db.relationship('LoginfoTable', backref='library', lazy=True)

    def __init__(self,book_name:str,edition_year:int,author:str,owner_name:str,category:str,translator:str):
        self.book_name    = book_name
        self.edition_year = edition_year
        self.author       = author
        self.owner_name   = owner_name
        self.category     = category
        self.translator   = translator
        self.date_time    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class LoginfoTable(db.Model):
    __tablename__ = "logTable"
    book_id_log   = db.Column(db.Integer, primary_key=True)
    date_time     = db.Column(db.String)
    process       = db.Column(db.String)
    owner         = db.Column(db.String)
    username      = db.Column(db.String)
    library_id    = db.Column(db.Integer, db.ForeignKey('libraryTable.book_id'))
    
    def __init__(self,process:str,owner:str,username:str,library_id:int):
        self.date_time  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.process    = process
        self.owner      = owner
        self.username   = username
        self.library_id = library_id

db.create_all()

