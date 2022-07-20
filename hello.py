from flask import Flask, flash, render_template, request
from flask_wtf import FlaskForm #framework for creating forms.
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError #Input box and submit button.
from wtforms.validators import DataRequired, EqualTo, Length #to validate wether input has been passed.
from datetime import datetime #import current time.
from flask_sqlalchemy import SQLAlchemy #import database.
from flask_migrate import Migrate #import stuff for migrating db.
from werkzeug.security import generate_password_hash, check_password_hash #stuff for hashing passwords.

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
    #adding new column
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #do some password stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Create a String.
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit
        flash("User Deleted Successfully!")
        
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)

    except:
        flash("Whoops! There was a problem deleting user, try again.") 
        return render_template("add_user.html", form=form, name=name, our_users=our_users)

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    #adding new line to form.
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()])
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
                name_to_update=name_to_update, id = id)
        except:
            flash("Error! Looks like there was a problem...try again.")
            return render_template("update.html", 
                form=form,
                name_to_update=name_to_update)
    else:
        return render_template("update.html", 
                form=form,
                name_to_update=name_to_update, id = id)
            
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
            #Hash the password.
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(
                name=form.name.data, 
                email=form.email.data, 
                favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            
            db.session.add(user)
            db.session.commit()
        
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        
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
