# intstall flask_sqlalchemy, sqlalchemy, mysqlclient

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




# ORM

# User  Modal or table
class User(db.Model):
    # creating columns
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(30))
    reg = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.reg = datetime.now()
    
    def __repr__(self):
        return f"<User {self.id}>"
    




# Go to home page
@app.route('/')
def index():
    # db.create_all()
    return render_template('index.html',  title = "Home")


# Go to contact page
@app.route('/contact')
def contact():
    return render_template('contact.html', title = "Contact")


# Go to about page
@app.route('/about')
def about():
    return render_template('about.html',  title = "About")


# Delete user
@app.route('/delete/<id>')
def delete(id):

    # Find user by id and delete user
    User.query.filter_by(id=id).delete()
    db.session.commit()

    # Get all users data
    users = User.query.all()

    # return to users page with users data
    return render_template('users.html', users=users,  title = "Users")



# Update user
@app.route('/edit_user/<id>', methods=["POST", "GET"])
def edit_user(id):

    # Check if form is submitted or posted
    if request.method == "POST":

        # Get form input values
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Update values
        user = User.query.filter_by(id=id).first()
        user.username = username
        user.email = email
        user.password = password
        db.session.commit()

        # read users
        users = User.query.all()
        return render_template('users.html', users=users, title = "Users")
    
    # fill edit user form
    user = User.query.filter_by(id=id).first()
    return render_template('editUser.html', user=user, title = "Edit user")



# Read all users
@app.route('/users')
def get_users():

    # get all users
    users = User.query.all()

    # return to users page with users data
    return render_template('users.html', users=users, title = "Users")


# create new user
@app.route('/add_user', methods=["POST", "GET"])
def add_user():

    # Check if form is submitted or posted
    if request.method == "POST":

        # Get form input values
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Create the new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Get all users
        users = User.query.all()

        # return to users page with users data
        return render_template('users.html' , users=users, title = "Users")

    # Go to create user form
    return render_template('createUser.html', title = "Create user")


if __name__ == "__main__":
    app.run()