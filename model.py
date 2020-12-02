

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
db = SQLAlchemy()


class User(db.Model):
    """A User"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
              autoincrement=True,
              primary_key=True)
    user_name = db.Column(db.String, unique=True)          
    email=db.Column(db.String, unique=True)
    password = db.Column(db.String)

    
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

    def __repr__(self):
        return f'<Room room_id={self.room_id} name={self.room_name}>'               

class Post(db.Model):
    """ A Post"""

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, 
                    autoincrement=True,
                      primary_key=True)
    image = db.Column(db.String)
    link =  db.Column(db.String)
    publish_date = db.Column(db.DateTime, server_default=func.now())
    post_title = db.Column(db.String)
    post_body = db.Column(db.String)
    image = db.Column(db.String)
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
    
    user = db.relationship('User', 
                            backref='posts')
    room = db.relationship('Room', backref='posts')
                             
    def __repr__(self):
        return f'<Post post_id={self.post_id} link={self.link}>'

class Like(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    
    user = db.relationship('User', backref='likes')
    post = db.relationship('Post', backref='likes')
    
    def __repr__(self):
        return f'<Like like_id={self.like_id}>'  


class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    name = db.Column(db.String, unique=True)
    
    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} text={self.text}>'

class Post_tag(db.Model):
    __tablename__ = 'post_tags'

    post_tag_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post = db.relationship('Post',  
                            backref='post_tags')
    
    tag = db.relationship('Tag', backref='post_tags')
    user = db.relationship("User", backref='post_tags')
    post = db.relationship('Post',  
                            backref='post_tags')
    def __repr__(self):
        return f'<Post_tag post_tag_id={self.post_tag_id}>'   

class Comment(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    comment_time = db.Column(db.DateTime)
    body = db.Column(db.String, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    
    user = db.relationship('User', backref='comments')
    post = db.relationship('Post',  
                            backref='comments')
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
   


        



