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

@app.route('/sign_up') 
def sign_up():

    render_template('sign_up.html', users=users)

@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user"""

    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again')
    else:
        crud.create_user(email, password)
        flash('Accoubt created! Please log in.') 
    return redirect('/sign_up')         


if __name__=="__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)