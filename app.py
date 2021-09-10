from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from tables import LibraryTable, LoginfoTable
from adminUsertables import Admin,User
# from flask_wtf import wtforms
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/turkai/Desktop/library/database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

@app.route("/", methods=["POST","GET"])
def index():
    if request.method== "POST":
        username = request.form["username"]
        password = request.form["password"]
        login = User.query.filter(userName=username, userPass=password).first()
        if login is not None:
            return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        userName    = request.form['userName']
        userSurname = request.form['userSurname']
        username2   = request.form['username2']
        email       = request.form['email']
        userPass    = request.form['userPass']

        user = User(userName=userName,userSurname=userSurname,username2=username2,email=email,userPass=userPass)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("listofBooks"))

    return render_template("signup.html")

@app.route("/books", methods=["GET","POST"])
def listofBooks():
    books = db.session.query(LibraryTable).all()
    return render_template("books.html")

@app.route("/addBook", methods=["POST","GET"]) 
# hata alıyorum add book yaparken
def addBook():
    if request.method == "POST":
        book_name    = request.form["book_name"]
        edition_year = request.form["edition_year"]
        author       = request.form["author"]
        owner_name   = request.form["owner_name"]
        category     = request.form["category"]
        translator   = request.form["translator"]

        book = LibraryTable(book_name,edition_year,author,owner_name,category,translator)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("listofBooks"))
        
    return render_template("addBook.html")

if __name__ == '__main__':
    app.run(host='192.168.1.134',debug=True,port=5000)
