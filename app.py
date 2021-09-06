from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from tables import LibraryTable, LoginfoTable


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home//Desktop/library/librarydatabase.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def listofBooks():
    book = LibraryTable(book_name="kitap ismi",edition_year=1999,author="yazar ismi",owner_name="sahibi",category="aaa",translator="çevirmen")
    db.session.add(book)
    db.session.commit()
    return render_template("book.html",book_ht=book)
