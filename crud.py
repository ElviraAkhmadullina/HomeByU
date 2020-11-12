"""CRUD operations"""

from model import db, User, Room, Post, Like, Tag, Post_tag, Comment, connect_to_db
from datetime import datetime



def create_user(user_name, email, password):
    """Create and Return new user"""

    user = User(user=user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_room(room_name):
    room = Room(name=room_name)

    db.session.add(room)
    db.session.commit()  

    return room_name

def create_post(user, room, link, release_date):     
    post=Post(user=user, room=room, link=link, 
            release_date=release_date)
    db.session.add(post)
    db.session.commit()
    return post

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

def create_post_tag(tag, post):
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