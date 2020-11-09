

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """A User"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
              autoincrement=True,
              primary_key=True)
    email=db.Column(db.String, unique=True)
    password = db.Column(db.String)

    post = db.relationship('Post')   

    def __repr__(self):
        """Show info about user"""

        return f'<User user_id={self.user_id} email={self.email}>'
        
        
class Room(db.Model):
    """A Room""" 

    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    room_name = db.Column(db.String, unique=True)

    post = db.relationship('Post') 

    def __repr__(self):
        return f'<Room room_id={self.room_id} name={self.room_name}>'               

class Post(db.Model):
    """ A Post"""

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    link =  db.Column(db.String)
    release_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
    
    room = db.relationship('Room')
    user = db.relationship('User')

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///rooms"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")






if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
   


        



