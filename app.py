from flask import Flask, render_template,request,redirect, sessions,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime, logging

from werkzeug.datastructures import Authorization
from tables import LibraryTable, LoginfoTable
from member import Member


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

@app.route("/", methods=["POST","GET"])
def index():
    try:
        if request.method == "POST":
            username = request.values.get("username")
            password = request.values.get("password")
           
            if username=="" or username==None or password=="" or password == None:
                return render_template("index.html", isAlert=True, alertMessage="Please enter your username and password.")
            else:
                nameQuery = db.session.query(Member.memberNick).filter(Member.memberNick==username).first()
                passQuery = db.session.query(Member.memberPass).filter(Member.memberPass==password).first()
                if nameQuery != None or passQuery != None:
                    if nameQuery[0] == username and passQuery[0] == password:
                        return redirect(url_for("listofBooks"))
                else:
                    return render_template("index.html", isAlert=True, alertMessage="Your username or password is wrong.")  
        else:
            return render_template("index.html", isAlert=False)
    except:
        return render_template("index.html", isAlert=False)



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



@app.route("/updatebook/<string:id>", methods=["GET","POST"])
def updateBook(id):
    if request.method == "POST":
        change_id = request.values.get("change_id")
        info      = request.values.get("info")
        
    #     if change_id == "1":
    #         query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         query.book_name = info
    #         queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         owner = queryOwner.owner_name
    #         log = LoginfoTable(process=f"Book name changed: {info}", owner=owner,library_id=id)
    #         db.session.add(log)
    #         db.session.commit()
    #         return redirect(url_for("listofBooks"))
            
    #     elif change_id == "2":
    #         query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         query.edition_year = info
    #         queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         owner = queryOwner.owner_name
    #         log = LoginfoTable(process=f"Book edition year changed: {info}", owner=owner, library_id=id)
    #         db.session.add(log)
    #         db.session.commit()
    #         return redirect(url_for("listofBooks"))

    #     elif change_id == "3":
    #         query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         query.author = info
    #         queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         owner = queryOwner.owner_name
    #         log = LoginfoTable(process=f"Book author changed: {info}",owner=owner, library_id=id)
    #         db.session.add(log)
    #         db.session.commit()
    #         return redirect(url_for("listofBooks"))

    #     elif change_id == "4":
    #         query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         query.owner_name = info
    #         queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         owner = queryOwner.owner_name
    #         log = LoginfoTable(process=f"Book owner name changed: {info}", owner=owner,library_id=id)
    #         db.session.add(log)
    #         db.session.commit()
    #         return redirect(url_for("listofBooks"))
            
    #     elif change_id== "5":
    #         query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         query.category = info
    #         queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         owner = queryOwner.owner_name
    #         log = LoginfoTable(process=f"Book category changed: {info}", owner=owner, library_id=id)
    #         db.session.add(log)
    #         db.session.commit()
    #         return redirect(url_for("listofBooks"))

    #     elif change_id == "6":
    #         query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         query.translator = info
    #         queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    #         owner = queryOwner.owner_name
    #         log = LoginfoTable(process=f"Book translator changed: {info}", owner=owner, library_id=id)
    #         db.session.add(log)
    #         db.session.commit()
    #         return redirect(url_for("listofBooks"))
    else:
        return render_template("updateBook.html")


@app.route("/deletebook/<string:id>", methods=["POST","GET"])
def deleteBook(id):
    if request.method == "POST":
        id = request.values.get("id")
        queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
        owner = queryOwner.owner_name
        log = LoginfoTable(process=f"Deleted {id}.book",owner=owner, library_id=id)
        queryDelete = db.session.query(LibraryTable).filter(LibraryTable.book_id==id).delete()
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("listofBooks"))
    else:
        return render_template("deleteBook.html")



if __name__ == '__main__':
    app.run(debug=True)
