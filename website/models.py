# database modelsssss

from . import db # init.py
from flask_login import UserMixin
from sqlalchemy.sql import func

# notes table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) # db will add this
    data = db.Column(db.String(10000)) # user input
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # db will add this
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # current_user will add this and db will pick up the relationship

# work table
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True) # db will create
    title = db.Column(db.String(200)) 
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # db will create
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    status = db.Column(db.String(100)) 
    points = db.Column(db.Integer)

# user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # created by db
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # store all notes user has, based on db relationship
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team_leader = db.Column(db.Boolean)
    work = db.relationship('Work') # store all work user has, based on db relationship
    points = db.Column(db.Integer)

# teams table
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = db.relationship('User') # store all users here

