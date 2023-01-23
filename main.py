# intstall flask_sqlalchemy, sqlalchemy, mysqlclient

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.debug = True


# ORM

# User  Modal
class User(db.Model):
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
        return f"<User {self.username}>"
    





@app.route('/')
def index():
    # db.create_all()
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


# Read all users
@app.route('/users')
def get_users():
    return render_template('users.html')


# create new user
@app.route('/add_user', methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        # print(f'username: {request.form["username"]}')
        # print(f'email: {request.form["email"]}')
        # print(f'password: {request.form["password"]}')
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('users.html')


    return render_template('createUser.html')


if __name__ == "__main__":
    app.run()