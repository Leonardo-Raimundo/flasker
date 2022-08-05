from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError #Input box and submit button.
from wtforms.validators import DataRequired, EqualTo, Length #to validate wether input has been passed.
from wtforms.widgets import TextArea

#create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Posts Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    #adding new line to form.
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Password Form
class PasswordForm(FlaskForm):
    email = StringField("What's your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit") 

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