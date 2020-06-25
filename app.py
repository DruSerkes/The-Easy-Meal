from flask import Flask, render_template, redirect, session, flash, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from forms import SignUpForm, LoginForm
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


#####################################
#     User Signup/Login/Logout      #
#####################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Handles user signup.
    GET Displays signup form 
    POST Creates/Adds new user to DB and redirects home
    """

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('You have been logged out', 'success')
    return redirect(url_for('homepage'))


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
