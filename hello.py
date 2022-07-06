from flask import Flask, render_template


#Create a Flask Instane
app = Flask(__name__) #helps Flask find our files on the directory

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

#returning index.html from templates folder.
def index():
    first_name = "John"
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