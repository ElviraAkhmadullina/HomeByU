"""Server for movie ratings app"""

from flask import (Flask, render_templates, request, flash, session, redirect) 
from model import connect_to_db
import crud

from jinja2 import StrictUnderfined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUnderfined

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

if __name__=="__main__":
    connect_to_db(app)
    app.run(host='o.0.0.0', debug=True)