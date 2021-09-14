from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from tables import LibraryTable, LoginfoTable
from member import Member


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/turkai/Desktop/library/database.db'

db = SQLAlchemy(app)

@app.route("/", methods=["POST","GET"])
def index():
    try:
        if request.method == "POST":
            username = request.values.get("username")
            password = request.values.get("password")
           
            if username==" " or password==" ":
                return render_template("index.html")
            else:
                nameQuery = db.session.query(Member.memberName).filter(Member.memberName==username).first()
                passQuery = db.session.query(Member.memberPass).filter(Member.memberPass==password).first()
                if nameQuery[0] == username and passQuery[0] == password:
                    return redirect(url_for("listofBooks"))
                else:
                    return render_template("index.html")  
        return render_template("index.html")
    except:
        return render_template("error.html")


@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        memberName    = request.values.get("memberName")
        memberSurname = request.values.get("memberSurname")
        memberNick    = request.values.get("memberNick")
        email         = request.values.get("email")
        memberPass    = request.values.get("memberPass")
        memberAuth    = request.values.get("memberAuth")

        member = Member(memberName=memberName,memberSurname=memberSurname,memberNick=memberNick,email=email,memberPass=memberPass, memberAuth=memberAuth)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for("listofBooks"))
    else:
        return render_template("signup.html")



@app.route("/books", methods=["GET","POST"])
def listofBooks():
    books = db.session.query(LibraryTable).all()
    return render_template("books.html", books=books)


@app.route("/addBook", methods=["POST","GET"]) 
def addBook():
    if request.method == "POST":
        book_name    = request.values.get("book_name")
        edition_year = request.values.get("edition_year")
        author       = request.values.get("author")
        owner_name   = request.values.get("owner_name")
        category     = request.values.get("category")
        translator   = request.values.get("translator")

        book = LibraryTable(book_name,edition_year,author,owner_name,category,translator)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("listofBooks"))
    return render_template("addBook.html")

@app.route("/updatebook", methods=["GET","POST"])
def updateBook():
    return render_template("updateBook.html")

if __name__ == '__main__':
    app.run(host='192.168.1.134',debug=True,port=5000)
