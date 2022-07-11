from flask import Flask, flash, render_template
from flask_wtf import FlaskForm #framework for creating forms.
from wtforms import StringField, SubmitField #Input box and submit button.
from wtforms.validators import DataRequired #to validate wether input has been passed.
from flask_sqlalchemy import SQLAlchemy #import database.
from datetime import datetime #import current time.

#Create a Flask Instane
app = Flask(__name__) #helps Flask find our files on the directory
#Add Database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key.
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know" #security measure for working with whatheforms.

db = SQLAlchemy(app)
#Create a Model.
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a String.
    def __repr__(self):
        return '<Name %r>' % self.name

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a route decorator
@app.route('/')

#def index():
#    return "<h1>Hello World!</h1>"

#filters
#safe
#capitalize
#lower
#upper
#tittle
#trim
#striptags

@app.route('/user/add', metho=['GET', 'POST'])
def add_user():
     return render_template("add_user.html") 

#returning index.html from templates folder.
def index():
    first_name = "Leonardo"
    #stuff = "This is <strong>Bold Text</strong>"
    stuff = "This is bold text"
    favorite_pizza = ["Pepperoni", "Cheese", "Musshroom", 41]
    return render_template("index.html", 
    first_name=first_name,
    stuff=stuff,
    favorite_pizza=favorite_pizza)

#localhost:5000/user/John
@app.route('/user/<name>') #<> allows us to pass a name on the url.

#returns passed name.
#def user(name):
#    return "<h1>Hello {}!!!</h1>".format(name)

def user(name):
    return render_template("user.html", user_name=name)

#Create custom error pages

#Invalid URL

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error thing
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validade Form
    if form.validate_on_submit(): #if someone submits a name, replace name = None with whatever name they passed.
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html",
        name = name,
        form = form)
