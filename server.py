

from flask import Flask, render_template, request, flash, session, redirect, g, jsonify, url_for
from model import db, User, Room, Post, Like, Tag, Post_tag, Comment, connect_to_db
from datetime import datetime
import datetime
from functools import wraps

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.logged_in:
            return redirect('login')
        return f(*args, **kwargs) 
    return decorated_function       

@app.before_request
def pre_process_all_requests():
    """Setup the request context"""

    user_id = session.get('user_id')
    current_user = User.query.get(user_id)
    if current_user:
        
        g.logged_in = True
        g.email = current_user.email
        g.user_id = current_user.user_id
        # Hashed passwords
        g.password = current_user.password
    else:
        g.logged_in = False
        g.email = None

@app.route('/')
def homepage():
    """View homepage"""
    
    return render_template('homepage.html')

@app.route('/unlike', methods=['POST'])
@login_required
def unlike_like():

    if g.logged_in:
        check = Like.query.filter(Like.user_id == g.user_id,
                                  Like.post_id == request.form.get('postId')
                                  ).first()
        if check:

            like = Like.query.filter(Like.user_id == g.user.id,
                                            Like.post_id == request.form.get('postId')
                                            ).first()
            db.session.delete(like)
            db.session.commit()
            return jsonify({'confirm': True, 'id': request.form.get('postId')}) 
        else:
            return jsonify({'confirm':'False'})                                                             


@app.route('/like', methods=['POST'])
@login_required
def like_an_post():

    if g.logged_in:
        check = Like.query.filter(Like.user_id == g.user_id,
                                   Like.post_id == request.form.get('postId')
                                    ).first()
    if not check:

        like = Like(user_id=g.user_id, post_id=request.form.get('postId'))

        db.session.add(like)
        db.session.commit()
        return jsonify({'confirm': True, 'id': request.form.get('postId')})
    else:
        return jsonify({'confirm': 'False'})                                    

@app.route('/timeline')
@login_required
def displey_users_timeline():
    
    posts_tags = Post_tag.query.filter(Post_tag.user_id == g.user_id).all()
    likes = Like.query.filter(Like.user_id == g.user_id).all()
    like_ids = [like.post_id for like in likes]

    tags = []
    for item in posts_tags:
        tags.append(item.tag_id)

    Post.query.filter(Post.tag_id.in_(tags),
                              ).order_by(Post.publish_date.desc()).all()
    return render_template('dashboard.html',
                             user=User.query.get(g.user_id),
                             posts_tags=posts_tags,
                             like_ids=like_ids)                             

@app.route('/add_tag', methods=['POST'])
@login_required
def follow_tag():

    if g.logged_in:
        check = Post_tag.query.filter(Post_tag.user_id == g.user_id,
                                       Post_tag.tag_id == request.form.get('add_tag')
                                         ).first()
        if not check:

            connection = Post_tag(post_id=g.user_id, tag_id=request.form.get('add_tag'))

            db.session.add(connection)
            db.session.commit()

    return redirect("/dashboard")     

@app.route('/remove_tag', methods=['POST'])
@login_required
def unfollow_tag():

    if g.logged_in:
        check = Post_tag.query.filter(Post_tag.user_id == g.user_id,
                                      Post_tag.tag_id == request.form.get('rem_tag')
                                      ).first()
        if check:

            tag = Post_tag.query.filter(Post_tag.user_id == g.user_id,
                                           Post_tag.tag_id == request.form.get('rem_tag')) .first()

            db.session.delete(tag)
            db.session.commit()

        return redirect('/dashboard')                                                                

@app.route('/dashboard')
@login_required 
def show_dashboard():
    
    post_tags = Post_tag.query.filter(Post_tag.user_id == g.user_id).all()

    followed_tags = []
    for each in post_tags:
        followed_tags.append(each.tag)

    all_tags = Tag.query.all()
    total_tags = []
    for each in all_tags:
        total_tags.append(each)
    
    not_followed_tags = []
    for each in total_tags:
        if each not in followed_tags:
            not_followed_tags.append(each)

    likes = Like.query.filter(Like.user_id == g.user_id).all()
    post = [{'post_body': text_from_html(like.post.post_body),
            'db_info': like.post} for like in likes]
    
    like_ids = [like.post_id for like in likes]
    return render_template('user_details.html', 
                        user=User.query.get(g.user_id),
                        post_tags=post_tags,
                        like_ids=like_ids,
                        not_followed_tags=not_followed_tags)

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

    likes = Like.query.filter(Like.user_id == g.user_id).all()

    like_ids = [like.post_id for like in likes]

    return render_template('post_details.html', 
                             user = User.query.get(g.user_id),
                             like_ids=like_ids,
                             post=post)


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