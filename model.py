

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

    comment = db.relationship('Comment', backref='users')

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

    post = db.relationship('Post', backref='rooms')
    
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
    
    comment = db.relationship('Comment', backref='posts')
    like = db.relationship('User', secondary='likes',
                            backref='posts')

    

                            
    def __repr__(self):
        return f'<Post post_id={self.post_id} link={self.link}>'

class like(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))


    def __repr__(self):
        return f'<Like like_id={self.like_id}>'  


class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    text = db.Column(db.String, unique=True)
    
    post_tag = db.relationship('Post', secondary = 'post_tags', 
                            backref='tags')
    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} text={self.text}>'

class Post_tag(db.Model):
    __tablename__ = 'post_tags'

    post_tag_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    

    def __repr__(self):
        return f'<Like like_id={self.like_id}>'   

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_time = db.Column(db.DateTime)
    body = db.Column(db.String, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    

    def __repr__(self):
        return f'<Tag post_id={self.post_id} body={self.body}>' 

             
           


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
   


        



