

from flask import (Flask, render_template, request, flash, session, redirect, g) 
from model import db, User, Room, Post, Like, Tag, Post_tag, Comment, connect_to_db
from datetime import datetime
import datetime
from functools import wraps

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

def login_required(decorated_view):
    @wraps(decorated_view)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            return redirect('/')
        return decorated_view(*args, **kwargs) 
    return decorated_function       

@app.before_request
def pre_process_all_requests():
    """Setup the request context"""

    user_id = session.get('user_id')
    if user_id:
        g.current_user = User.query.get(user_id)
        g.logged_in = True
        g.email = g.current_user.email
        g.user_id = g.current_user.user_id
        # Hashed password
        g.password = g.current_user.password
    else:
        g.logged_in = False
        g.current_user = None
        g.email = None

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html', user=g.current_user)


@app.route('/create_post')
def show_create_post_form():
    rooms = Room.query.all()
    
    for room in rooms:
        print(room)

    return render_template('create_post.html', rooms=rooms)

@app.route('/rooms')
def all_rooms():
    """View all rooms"""

    rooms = Room.query.all()

    return render_template('all_rooms.html', rooms=rooms)


@app.route('/posts')
def all_posts():
    """View all posts"""

    posts = Post.query.all() 

    return render_template('all_posts.html', posts=posts) 

@app.route('/posts/<post_id>')
def show_posts(post_id): 
    """ Show a particular post"""

    post = Post.query.get(post_id)

    return render_template('post_details.html', post=post)


@app.route('/submit_post', methods=['POST'])
def submit_post():
    print(request.form)

    room_id = request.form.get('room_id')
    link = request.form.get('link')
    post_title = request.form.get('post_title')
    post_body = request.form.get('post_body')
    image = request.form.get('image')
    user_id = session.get('user_id')
    user = User.query.filter(User.user_id == user_id).first()
    room = Room.query.get(room_id) 

    
    post=Post(user=user, room=room, link=link, 
            post_title=post_title, 
            post_body=post_body, image=image)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post.post_id}")

@app.route('/dashboard')
@login_required 
def show_dashboard():
    post_tags = Post_tag.query.filter(Post_tag.user_id == g.user_id).all()

    all_tags = Tag.query.all()
    total_tags = []
    for each in all_tags:
        total_tags.append(each)

    return render_template('dashboard.html', 
                        user=g.current_user,
                        posts_tags=post_tags)

@app.route('/register_page', methods=['GET']) 

def show_login_and_register():

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register_user():
    """Create a new user"""
    #Get the user's name, email and password from the form
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    tags = request.form.getlist("tag")
    #Chek whether the user exist
    user = User.query.filter(User.email == email).first()
    
    if user:
        flash('{} Already exist. Please log in'.format(email))
        return redirect("/login")
    else:
        user = User(user_name=user_name, email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        for tag in tags:
            connection = Post_tag(user_id=user.user_id, tag_id=int(tag))
            db.session.add(connection)
            db.session.commit()
        session['user_id'] = user.user_id        
        return redirect('/dashboard')
        
@app.route('/login', methods=['GET'])
def login_form():

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_user():

    email = request.form.get('email') 
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    # If the password matches the user's password, log in
    # otherwise don't let them log in
    if user.password == password:
        flash('Welcome Back!')
        session['user_id'] = user.user_id
        return redirect("/dashboard")

    flash("No account by that name! Please create an account!") 
    
    return redirect('/login')            

@app.route('/logout')
def logout():
    session.clear()
    flash("See you later!")

    return redirect("login.html")

if __name__=="__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)