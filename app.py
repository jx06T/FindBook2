from flask_sqlalchemy import SQLAlchemy
from flask import Flask , session ,request, redirect,url_for, render_template
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'mysecretkey'
class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    email = db.Column(db.String(100))
    def __init__(self, name, email):
        self.name =name
        self.email = email

_id = db.Column('id', db.Integer, primary_key=True)
name = db.Column('name', db.String(100))
email = db.Column(db.String(100))

@app.route("/user", methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email =  request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user).first()    
            found_user.email = email
            db.session.commit()
          
        else:
            if "email" in session:
                email = session["email"]
            
            
        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        found_user = Users.query.filter_by(name=user).first()        
        if found_user:
            session["email"]= found_user.email            
        else:
            usr = Users(user,"")
            db.session.add(usr)
            db.session.commit()
         
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))        
        return render_template("login.html")

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)