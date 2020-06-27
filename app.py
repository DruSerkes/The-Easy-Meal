from flask import Flask, render_template, redirect, session, flash, jsonify, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Recipe, Ingredient, GroceryList, Step
from forms import SignupForm, LoginForm, GroceryListForm
from helpers import generate_login_data, generate_user_data
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', "postgres:///easymeal")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', "easysecretmeal")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

CURR_USER_KEY = "user_id"


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

    form = SignupForm()

    if form.validate_on_submit():
        user_data = generate_user_data(form)
        try:
            user = User.signup(user_data)
            db.session.add(user)
            db.session.commit()

        except IntegrityError as error:
            db.session.rollback()
            if (f'(username)=({user.username}) already exists') in error._message():
                flash("Username already taken", 'danger')
            elif (f'(email)=({user.email}) already exists') in error._message():
                flash("Email already taken", 'danger')

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
        data = generate_login_data(form)
        user = User.authenticate(data)

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
    return redirect(url_for('home_page'))


########################
#       Routes         #
########################


@app.route('/')
def home_page():
    """ Home Page """
    return render_template('index.html')


########################
#      User Routes     #
########################

@app.route('/users/<int:id>')
def view_profile(id):
    """ Dispay user profile """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))
    
    return render_template('users/profile.html')


@app.route('/favorites/<int:id>')
def view_saved_recipes(id):
    """ Route to view saved recipes """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login')) 

    return render_template('users/favorites.html')


@app.route('/recipes/<int:id>')
def view_recipe_details(id):
    """ View recipe in detail """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    recipe = Recipe.query.get_or_404(id)
    return render_template('recipes/details.html', recipe=recipe)


########################
# Grocery List Routes  #
########################

@app.route('/groceries')
def view_grocery_list():
    """ View current grocery list """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    grocery_list = GroceryList.query.order_by('date_created desc').limit(1)
    return render_template('users/groceries.html', grocery_list=grocery_list)


# TODO
@app.route('/groceries/history')
def view_list_history():
    """ View grocery lists """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    return "All grocery lists"



# Check if user has a grocery list - if not, create a grocery list associated with this user with default title
# For every ingredient coming from the currently viewed recipe, check if it's already on the list - if not, add it to the list! 
# Return JSON of the created w/201 or updated grocery list w/200  
@app.route('/groceries', methods=['POST'])
def add_ingredients_to_list():
    """ 
    Expects JSON
    Creates a grocery list 
    Returns JSON of created list and success message.  
    """
    # Check if authorized
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))
    # Make a grocery list if user doesn't already have one
    if len(g.user.grocery_lists) == 0:
        new_list = GroceryList(user_id=g.user.id)
        db.session.add(new_list)
        db.session.commit()
    # Grab most recent grocery list and recipe being added 
    grocery_list = GroceryList.query.filter(GroceryList.user_id == g.user.id).order_by('date_created desc').limit(1)
    recipe = Recipe.query.get_or_404(request.json['id'])
    # Add recipe ingredients to grocery list if they're not already there
    for ingredient in recipe.ingredients:
        if ingredient not in grocery_list.ingredients:
            grocery_list.ingredients.append(ingredient)
    db.session.commit()
    # Return JSON response 
    response_json = jsonify(grocery_list=grocery_list.serialize(), message="Ingredients Added!")
    return (response_json, 201)
    






########################
#     Custom Errors    #
########################
# CUSTOM 404 PAGE
@app.errorhandler(404)
def display_404(error):
    """ Displays a custom error page when returning a 404 error """
    return render_template('errors/error404.html'), 404


# CUSTOM 401 PAGE
@app.errorhandler(401)
def display_401(error):
    """ Displays a custom error page when returning a 401 error """
    return render_template('errors/error401.html'), 401


# CUSTOM 500 PAGE
@app.errorhandler(500)
def display_500(error):
    """ Displays a custom error page when returning a 500 error"""
    return render_template('errors/error500.html'), 500
