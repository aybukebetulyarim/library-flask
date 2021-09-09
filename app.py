from flask import Flask, render_template,request,redirect,url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from tables import LibraryTable, LoginfoTable


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/turkai/Desktop/library/librarydatabase.db'

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    return render_template("signup.html")

@app.route("/books", methods=["POST"])
def listofBooks():
    book = LibraryTable(book_name="kitap ismi",edition_year=1999,author="yazar ismi",owner_name="sahibi",category="aaa",translator="çevirmen")
    # db.session.add(book)
    books = db.session.query(LibraryTable).all()
    db.session.commit()
    return render_template("books.html",books=books)

@app.route("/addBook", methods=["POST","GET"])
def addBook():
    return render_template("addBook.html")

if __name__ == '__main__':
    app.run(host='192.168.1.134',debug=True,port=5000)

 