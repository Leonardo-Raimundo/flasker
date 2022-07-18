from flask import Flask, flash, render_template, request
from flask_wtf import FlaskForm #framework for creating forms.
from wtforms import StringField, SubmitField #Input box and submit button.
from wtforms.validators import DataRequired #to validate wether input has been passed.
from datetime import datetime #import current time.
from flask_sqlalchemy import SQLAlchemy #import database.
from flask_migrate import Migrate

#Create a Flask Instane
app = Flask(__name__) #helps Flask find our files on the directory
#Add Database.
#Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#New MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/our_users'

#Secret Key.
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know" #security measure for working with whatheforms.

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Create a Model.
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #adding new column
    favorite_color = db.Column(db.String(120))
    #Create a String.
    def __repr__(self):
        return '<Name %r>' % self.name

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    #adding new line to form.
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

#Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']

        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", 
                form=form,
                name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem...try again.")
            return render_template("update.html", 
                form=form,
                name_to_update=name_to_update)
    else:
        return render_template("update.html", 
                form=form,
                name_to_update=name_to_update)
            
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

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit(): #if someone submits a name, replace name = None with whatever name they passed.
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users) 
        
        

#Create a route decorator
@app.route('/')

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
