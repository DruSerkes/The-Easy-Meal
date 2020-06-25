from flask import Flask, render_template, redirect, session, flash, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from forms import RegisterForm, LoginForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', "postgres:///easymeal")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', "easysecretmeal")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


########################
#       Routes         #
########################


@app.route('/')
def home_page():
    """ Home Page """
    return render_template('index.html')


########################
#     Custom Errors    #
########################

# CUSTOM 404 PAGE
@app.errorhandler(404)
def display_404(error):
    """ Displays a custom error page when returning a 404 error """
    return render_template('error.html'), 404


# CUSTOM 401 PAGE
@app.errorhandler(401)
def display_401(error):
    """ Displays a custom error page when returning a 404 error """
    return render_template('error401.html'), 401
