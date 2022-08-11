import email
from flask import Flask, flash, redirect, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from pymysql import Date
from sqlalchemy import PrimaryKeyConstraint #framework for creating forms.
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError #Input box and submit button.
from wtforms.validators import DataRequired, EqualTo, Length #to validate wether input has been passed.
from datetime import datetime #import current time.
from flask_sqlalchemy import SQLAlchemy #import database.
from flask_migrate import Migrate #import stuff for migrating db.
from werkzeug.security import generate_password_hash, check_password_hash #stuff for hashing passwords.
from datetime import date
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm 

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

#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Sucessful!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try again!")
        else:
            flash("That user doesn't exit - Try again!")

    return render_template('login.html', form=form)

#create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out. Thanks for stopping by!")
    return redirect(url_for('login'))

#create dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']

        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update, id = id)
        except:
            flash("Error! Looks like there was a problem...try again.")
            return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update)
    else:
        return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update, id = id)
    
    return render_template('dashboard.html')



@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            #return a message
            flash("Blog post was deleted!")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
        
        except:
            #return an error messsage
            flash("Whoops! There was a problem deleting the post. Try again!")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("You aren't authorized to delete that post!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

@app.route('/posts')
def posts():
    #grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        #post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        #Updata database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form = form)
    else:
        flash("You aren't authorized to edit this post!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
#Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
            title=form.title.data, 
            content=form.content.data,
            poster_id = poster,
            slug=form.slug.data)
        #Clear the form
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
        form.slug.data = ''

        #Add post data to database
        db.session.add(post)
        db.session.commit()

        #return a message
        flash("Blog Post Submitted Successfully!")

    #return to the web page
    return render_template("add_post.html", form=form)

#Json Thing
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "Leonardo": "Bacon",
        "Joana": "Pepperoni",
        "Frida": "Fish"
    }
    return favorite_pizza
    #return {"Date": date.today()}

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

#Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']

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
                username=form.username.data, 
                email=form.email.data, 
                favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            
            db.session.add(user)
            db.session.commit()
        
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
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

#Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    #Validade Form
    if form.validate_on_submit(): #if someone submits a name, replace name = None with whatever name they passed.
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        
        #Lookup user by email adress.
        pw_to_check = Users.query.filter_by(email=email).first()
        
        #Check hashed password.
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html",
        email = email,
        password = password,
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)

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

#Create a Model.
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    #adding new column
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #do some password stuff!
    password_hash = db.Column(db.String(128))
    # User can have many posts
    posts = db.relationship('Posts', backref='poster')

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

#Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    #author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign key to link user (refer to the primary key of the user)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))