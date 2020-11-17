# """Server for movie ratings app"""

from flask import (Flask, render_template, request, flash, session, redirect) 
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    
    if "user_id" in session:
        return redirect('/dashboard')

    return render_template('homepage.html')

@app.route('/dashboard')
def show_dashboard():
    if "user_id" not in session:
        flash("Please log in!")
        return redirect("/")

    return render_template('dashboard.html')


@app.route('/register_page') 
def show_login_and_register():

    return render_template('login.html')
    

@app.route('/create_post')
def show_create_post_form():
    rooms = crud.get_rooms()
    
    print("\n\n\nAll the rooms:")
    for room in rooms:
        print(room)

    return render_template('create_post.html', rooms=rooms)

@app.route('/rooms')
def all_rooms():
    """View all rooms"""

    rooms = crud.get_rooms()

    return render_template('all_rooms.html', rooms=rooms)

@app.route('/posts')
def all_posts():
    """View all posts"""

    posts = crud.get_posts()

    return render_template('all_posts.html', posts=posts)    

@app.route('/user', methods=['POST'])
def register_user():
    """Create a new user"""

    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Already exist')
    else:
        crud.create_user(user_name,email, password)
        flash('Account created! Please log in.') 
    return redirect('/')    

@app.route('/login', methods=['POST'])
def login_user():

    email = request.form.get('email') 
    password = request.form.get('password')
    print(f'\n\n\n\n\nEmail is = {email}')

    user = crud.get_user_by_email(email)

    # If the password matches the user's password, log in
    # otherwise don't let them log in
    if user.password == password:
        flash('Welcome Back!')
        session['user_id'] = user.user_id
    else:
        flash("No account by that name! Please create an account!") 
    
    return redirect('/')            



if __name__=="__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)