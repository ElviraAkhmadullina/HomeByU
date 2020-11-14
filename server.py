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

    return render_template('homepage.html')

@app.route('/login') 
def sign_up():

    render_template('login.html')

@app.route('/users', methods=['POST'])
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
        flash('Accoubt created! Please log in.') 
    return redirect('/login')         

# @app.route('/post_form', method=[POST])
# def create_post():


#     return render_template('post_form.html')

if __name__=="__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)