"""CRUD operations"""

from model import db, User, Room, Post, Like, Tag, Post_tag, Comment, connect_to_db
from datetime import datetime



def create_user(user_name, email, password):
    """Create and Return new user"""

    user = User(user_name=user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """Return all users"""
    return User.query.all()

def get_user_by_id(user_id):

    return User.query.filter(User.user_id == user_id).first()    

def get_user_by_email(email):
    """Return user by email"""

    return User.query.filter(User.email == email).first()

def get_user_by_password(password):
    """Return user by password"""

    return User.query.filter(User.password == password).first()

def get_user_by_user_name(user_name):
    return User.query.filter(User.user_name == user_name).first()


def create_room(room_name):
    
    room = Room(room_name=room_name)

    db.session.add(room)
    db.session.commit()  

    return room


def get_rooms():

    return Room.query.all()


def get_room_by_id(room_id):

    return Room.query.get(room_id)    


def create_post(user, room, link, 
                  post_title, post_body, image):     
    
    post=Post(user=user, room=room, link=link, 
            post_title=post_title, 
            post_body=post_body, image=image)
    db.session.add(post)
    db.session.commit()
    return post

def get_posts():
    """Return all posts"""

    return Post.query.all() 

def get_post_by_id(post_id):

    return Post.query.get(post_id)

def create_like(user, post):
    like=Like(user=user, post=post)
    db.session.add(like)
    db.session.commit()
    
    return like

def create_tag(text):
    tag=Tag(text=text)
    db.session.add(tag)
    db.session.commit()    
    
    return tag
def create_user(user_name, email, password):
    """Create and Return new user"""

    user = User(user_name=user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_post_tag(tag_id, user_id, post_id):
    post_tag=Post_tag(tag=tag, post=post)
    db.session.add(post_tag)
    db.session.commit()
    
    return Post_tag

def create_comment(user, post, body):
    comment=Comment(user=user, post=post, body=body)
    db.session.add(comment)
    db.session.commit()    

    return comment

if __name__ == '__main__':
    from server import app
    connect_to_db(app)               