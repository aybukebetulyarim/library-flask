from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from tables import LibraryTable, LoginfoTable
from adminUsertables import Admin,User

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/turkai/Desktop/library/librarydatabase.db'

db = SQLAlchemy(app)

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("password")
        if username==" " or password==" ":
            return render_template("index.html")
        else:
            nameQuery = User.query.filter(User.userName==username).first()
            passQuery = User.query.filter(User.userPass==password).first()
            print(nameQuery)
            print(passQuery)

            if username == nameQuery and password == passQuery:
                print(username)
                print(password)
                return render_template("books.html")
            else:
                return render_template("index.html", username=username, password=password)
    return render_template("index.html")



@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        userName    = request.form["userName"]
        userSurname = request.form["userSurname"]
        username2   = request.form["username2"]
        email       = request.form["email"]
        userPass    = request.form["userPass"]
        user = User(userName = userName,userSurname=userSurname,username2=username2,email=email,userPass=userPass)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("listofBooks"))
    else:
        return render_template("signup.html")

@app.route("/books", methods=["GET","POST"])
def listofBooks():
    books = db.session.query(LibraryTable).all()
    return render_template("books.html")


@app.route("/addBook", methods=["POST","GET"]) 
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
