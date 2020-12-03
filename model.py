"""Models and database functions for my project."""

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
    user_name = db.Column(db.String(50), unique=True, nullable=False)          
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    avatar = db.Column(db.String, default="Users-User-Female-icon.png")
    background_img = db.Column(db.String, default="fog-56a407943df78cf772806f75.jpg")
    
    
    def __repr__(self):
    
     """Show info about user"""
     
     return f'<User user_id={self.user_id} email={self.email}>'
        
        
class Blog(db.Model):
    """Blog which users follow""" 

    __tablename__ = 'blogss'

    blog_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rss_url = db.Column(db.String(200), nullable=False)
    blog_url = db.Column(db.String(100), nullable=False)
    build_date = db.Column(db.String(100), nullable=True)
    most_recent = db.Column(db.String(100), nullable=True)
    def __repr__(self):
        return f'<Room room_id={self.room_id} name={self.room_name}>'               

class Article(db.Model):
    """ Articles from rss feeds of blogs that my users follow"""

    __tablename__ = 'articles'
    
    article_id = db.Column(db.Integer, 
                    autoincrement=True,
                      primary_key=True)
    title = db.Column(db.String, nullable=False)
    publish_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    link =  db.Column(db.String, nullable=False)
    activity = db.Column (db.Boolean, default = True)
    description = db.Column(db.String, nullable = True)
    content = db.Column(db.String, nullable=True)
    
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'))
    
    blog = db.relationship('Blog', backref='blogs')
                             
    def __repr__(self):
        return f'<Post post_id={self.post_id} link={self.link}>'

class Like(db.Model):
    "Favorite articles"

    __tablename__ = 'likes'
    __table_args__ = (db.UniqueConstaint('user_id', 'article_id'),)
    
    like_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    hidden = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'), nullable=False)
    
    user = db.relationship('User', backref='likes')
    article = db.relationship('Article', backref='likes')
    
    def __repr__(self):
        return f'<Like like_id={self.like_id}>'  


class User_blog(db.Model):
    "Association table between users and blogs"

    __tablename__ = 'user_blogs'

    user_blog_id = db.Column(db.Integer, 
                    autoincrement=True,
                     primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'))
    
    user = db.relationship("User", backref='user_blogs')
    blog = db.relationship('Blog',  
                            backref='user_blogs')
    def __repr__(self):
        return f'<User_blog_id={self.user_blog_id}>'   
      


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
   


        



