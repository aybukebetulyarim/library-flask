from flask import Flask, render_template,request,redirect, session,url_for
from flask_sqlalchemy import SQLAlchemy
from tables import LibraryTable, LoginfoTable
from member import Member 
import bcrypt


app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datab.db'

db = SQLAlchemy(app)

@app.route("/", methods=["POST","GET"])
def index():
    try:
        if request.method == "POST":
            username = request.values.get("username")
            password = request.values.get("password").encode('utf-8')
            auth     = request.values.get("memberAuth")
            
            if username=="" or username==None or password=="" or password == None:
                return render_template("index.html", isAlert=True, alertMessage="Please enter your username and password.")
            else:
                nameQuery = db.session.query(Member.memberNick).filter(Member.memberNick==username).first()
                passQuery = db.session.query(Member.memberPass).filter(Member.memberNick==username).first()
                authQuery = db.session.query(Member.memberAuth).filter(Member.memberNick==username).first()
                print(authQuery[0])
                if bcrypt.checkpw(password, passQuery[0]) and nameQuery[0] == username:
                    if authQuery[0]==auth and auth =="1":
                        session["username"] = username
                        session["password"] = password
                        return redirect(url_for("listofBooks"))
                    elif authQuery[0]==auth and auth=="0":
                        return render_template("user.html")
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
        hashed        = bcrypt.hashpw(memberPass.encode('utf-8'), bcrypt.gensalt())
        memberAuth    = request.values.get("memberAuth")
        member = Member(memberName=memberName,memberSurname=memberSurname,memberNick=memberNick,email=email,memberPass=hashed, memberAuth=memberAuth)
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
        query = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
        queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
        owner = queryOwner.owner_name
        username_session = session.get("username")
        print(username_session)
        if change_id == "1":
            old_version = query.book_name
            query.book_name = info
            log = LoginfoTable(process=f"book_name {old_version}->{info}", owner=owner, username=username_session,library_id=id)
            db.session.add(log)
            db.session.commit()
        elif change_id == "2":
            old_version = query.edition_year
            query.edition_year = info
            log = LoginfoTable(process=f"edition_year {old_version}->{info}", owner=owner,username=username_session,library_id=id)
            db.session.add(log)
            db.session.commit()
        elif change_id == "3":
            old_version = query.author
            query.author = info
            log = LoginfoTable(process=f"author {old_version}->{info}", owner=owner,username=username_session,library_id=id)
            db.session.add(log)
            db.session.commit()
        elif change_id == "4":
            old_version = query.owner_name
            query.owner_name = info
            log = LoginfoTable(process=f"owner_name {old_version}->{info}", owner=info,username=username_session,library_id=id)
            db.session.add(log)
            db.session.commit()
        elif change_id == "5":
            old_version = query.category
            query.category = info
            log = LoginfoTable(process=f"category {old_version}->{info}", owner=owner,username=username_session,library_id=id)
            db.session.add(log)
            db.session.commit()
        elif change_id == "6":
            old_version = query.translator
            query.translator = info
            log = LoginfoTable(process=f"translator {old_version}->{info}", owner=owner,username=session.get("username"),library_id=id)
            db.session.add(log)
            db.session.commit()
        return redirect(url_for("listofBooks"))
    return render_template("updateBook.html")


@app.route("/books/<string:id>")
def deleteBook(id):
    queryOwner = db.session.query(LibraryTable).filter(LibraryTable.book_id == id).first()
    owner = queryOwner.owner_name
    log = LoginfoTable(process=f"Deleted {id}, owner->{owner}",owner=owner, username= session.get("username"),library_id=id)
    db.session.query(LibraryTable).filter(LibraryTable.book_id==id).delete()
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('listofBooks'))

@app.route("/log")
def log():
    log = db.session.query(LoginfoTable).all()
    return render_template("log.html", logs=log)

if __name__ == '__main__':
    app.run(debug=True)
