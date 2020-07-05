from flask import Flask, render_template, redirect, session, request, flash, jsonify, url_for, abort, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Recipe, Ingredient, GroceryList, Step, Measurement, UserRecipe
from forms import SignupForm, LoginForm, GroceryListForm
from helpers import generate_login_data, generate_user_data, generate_headers, generate_search_params, add_and_commit, get_recipe, do_search, add_ingredients_to_db, add_measurement_for_ingredient, add_recipe_to_db, valid_cuisines, valid_diets, do_logout, do_login
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
# from secrets import app_password, api_key, student_key
import requests
import os

app = Flask(__name__)
if __name__ == '__main__':
    app.run()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', "postgres:///easymeal")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = (
    'Easy Meals', 'EasyMealsOfficial@gmail.com')
app.config['MAIL_USERNAME'] = 'EasyMealsOfficial@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['app_password']
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = False  # Set to false once in production
app.config['MAIL_MAX_EMAILS'] = 1
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', "easysecretmeal")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)
mail = Mail(app)
connect_db(app)
db.create_all()

CURR_USER_KEY = "user_id"
# API_BASE_URL = "https://api.spoonacular.com"
API_BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
# API_KEY = api_key
API_KEY = student_key

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

    g.valid_cuisines = [cuisine for cuisine in valid_cuisines]
    g.valid_diets = [diet for diet in valid_diets]


@app.context_processor
def context_processor():
    """ Process global context for jinja templates """
    return dict(cuisines=valid_cuisines, diets=valid_diets)


@ app.route('/signup', methods=["GET", "POST"])
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
            add_and_commit(user)
            grocery_list = GroceryList.create(user.id)
            add_and_commit(grocery_list)

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


@ app.route('/login', methods=["GET", "POST"])
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


@ app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('You have been logged out', 'success')
    return redirect(url_for('home_page'))


########################
#     Search Routes    #
########################


@ app.route('/')
def home_page():
    """ Home Page """
    if not g.user:
        return redirect(url_for('signup'))

    response = do_search(request)
    data = response.json()
    recipes = data['results']
    id_list = [recipe.id for recipe in g.user.recipes]

    return render_template('index.html', data=data, recipes=recipes, id_list=id_list, diets=g.valid_diets, cuisines=g.valid_cuisines)


@ app.route('/load')
def load():
    """
    Load more results when user hits the end of the page
    Expects arg offset to query API for the next 12 results based on the search query information
    Returns the api response data
    """
    if request.args:
        response = do_search(request)
        data = response.json()

        if len(data['results']) == 0:
            return (jsonify(data=data), 200)

        user_favorites = [f.id for f in g.user.recipes]
        favorites = [r['id']
                     for r in data['results'] if r['id'] in user_favorites]
        response_json = jsonify(data=data, favorites=favorites)

    return (response_json, 200)


@ app.route('/search')
def search_recipes():
    """ Search for a recipe based on user input """
    if not g.user:
        return abort(401)

    response = do_search(request)
    data = response.json()

    if len(data['results']) == 0:
        return (jsonify(data=data), 200)

    user_favorites = [f.id for f in g.user.recipes]
    favorites = [r['id'] for r in data['results'] if r['id'] in user_favorites]
    response_json = jsonify(data=data, favorites=favorites)

    return (response_json, 200)


########################
#      User Routes     #
########################


@ app.route('/users/<int:id>')
def view_user(id):
    """ Dispay user profile """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    return render_template('users/profile.html')


@ app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    """ Update user info """
    if not g.user:
        return abort(401)
    if request.json['id'] != id:
        return jsonify(errors="You don't have permission to do that!")

    try:
        user = User.query.get_or_404(id)
        new_email = request.json.get('email', user.email)
        new_img_url = request.json.get('imgUrl', user.img_url)
        if new_email:
            user.email = new_email
        if new_img_url:
            user.img_url = new_img_url

        db.session.commit()

        response_json = jsonify(user=user.serialize(),
                                message="Update successful!")
        return (response_json, 200)
    except Exception as e:
        return jsonify(errors=str(e))


@ app.route('/favorites/<int:id>', methods=['POST'])
def add_favorite(id):
    """ Favorite a recipe """
    if not g.user:
        return abort(401)

    recipe = Recipe.query.filter_by(id=id).first()

    if not recipe:
        response = get_recipe(id)
        data = response.json()

        recipe = add_recipe_to_db(data)
        g.user.recipes.append(recipe)
        db.session.commit()
    else:
        g.user.recipes.append(recipe)
        db.session.commit()

    response_json = jsonify(
        recipe=recipe.serialize(), message="Recipe Added!")
    return (response_json, 200)


@ app.route('/favorites/<int:id>', methods=['DELETE'])
def remove_favorite(id):
    """ Unfavorite a recipe """
    if not g.user:
        return abort(401)
    try:
        recipe = Recipe.query.filter_by(id=id).first()
        UserRecipe.query.filter(
            UserRecipe.user_id == g.user.id, UserRecipe.recipe_id == recipe.id).delete()
        db.session.commit()
        response_json = jsonify(recipe=recipe.serialize(),
                                message="Recipe removed!")
        return (response_json, 200)
    except Exception as e:
        print(str(e))
        return jsonify(errors=str(e))


########################
#    Recipe Routes     #
########################


@ app.route('/favorites/')
def view_saved_recipes():
    """ Route to view saved recipes """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    id_list = [recipe.id for recipe in g.user.recipes]

    return render_template('users/favorites.html', id_list=id_list)


@ app.route('/recipes/<int:id>')
def view_recipe_details(id):
    """ View recipe in detail """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        response = get_recipe(id)
        data = response.json()
        return render_template('recipes/details.html', recipe=data)
    else:
        return render_template('recipes/details.html', recipe=recipe)


########################
# Grocery List Routes  #
########################


@ app.route('/groceries')
def view_grocery_list():
    """ View a grocery list """
    if not g.user:
        flash('You must be logged in to do that', 'warning')
        return redirect(url_for('login'))

    grocery_list = GroceryList.query.filter(
        GroceryList.user_id == g.user.id).first()
    return render_template('groceries/list.html', grocery_list=grocery_list)


@ app.route('/groceries', methods=['POST'])
def add_ingredients_to_list():
    """
    Expects JSON with recipe id
    Creates grocery list if one is not already associated with this user.
    Adds ingredients to most recently created grocery list
    Returns JSON of created list and success message.
    """
    # Check if authorized
    if not g.user:
        return abort(401)
    # Make a grocery list if user doesn't already have one
    if not g.user.grocery_list:
        new_list = GroceryList(user_id=g.user.id)
        db.session.add(new_list)
        db.session.commit()
    # Grab most recent grocery list and recipe being added
    grocery_list = GroceryList.query.filter_by(user_id=g.user.id).order_by(
        GroceryList.date_created.desc()).first()
    recipe = Recipe.query.get_or_404(request.json['id'])
    # Add recipe ingredients to grocery list if they're not already there
    for ingredient in recipe.ingredients:
        if ingredient not in grocery_list.ingredients:
            grocery_list.ingredients.append(ingredient)
    db.session.commit()
    # Return JSON response
    response_json = jsonify(
        grocery_list=grocery_list.serialize(), message="Ingredients Added!")
    return (response_json, 200)


@app.route('/groceries/<int:list_id>', methods=['POST'])
def add_one_ingredient_to_list(list_id):
    """ Add a single ingredient to users grocery list """
    if not g.user:
        return abort(401)
    grocery_list = GroceryList.query.get_or_404(list_id)
    ingredient = request.json.get('ingredient', None)

    if ingredient:
        ingredients = session.get('ingredients', [])
        ingredients.append(ingredient)
        session['ingredients'] = ingredients

    response_json = jsonify(ingredient=ingredient)
    return (response_json, 201)


@ app.route('/groceries/<int:list_id>', methods=['PATCH'])
def remove_ingredient_from_list(list_id):
    """
    Expects JSON with ingredient ID
    Removes ingredient from grocery list
    Returns JSON of update Grocery List and success message
    """
    if not g.user:
        return abort(401)

    grocery_list = GroceryList.query.get_or_404(list_id)

    if not request.json['id']:
        ingredients = session.get('ingredients', [])
        i_to_remove = request.json['ingredient']
        ingredients.remove(i_to_remove)
        session['ingredients'] = ingredients
        response_json = jsonify(
            grocery_list=grocery_list.serialize(), message="List updated!")
        return (response_json, 200)

    i_to_remove = Ingredient.query.get_or_404(request.json['id'])

    for ingredient in grocery_list.ingredients:
        if ingredient == i_to_remove:
            grocery_list.ingredients.remove(ingredient)
            break
    db.session.commit()

    response_json = jsonify(
        grocery_list=grocery_list.serialize(), message="List updated!")
    return (response_json, 200)


@ app.route('/groceries/<int:list_id>', methods=['DELETE'])
def empty_list(list_id):
    """ Remove all ingredients from a grocery list """
    if not g.user:
        return abort(401)
    try:
        grocery_list = GroceryList.query.get_or_404(list_id)
        grocery_list.ingredients = []
        db.session.commit()

        session['ingredients'] = []

        response_json = jsonify(message="Your list has been cleared!")
        return (response_json, 200)
    except Exception as e:
        db.session.rollback()
        return jsonify(errors=str(e))


@ app.route('/email/<int:list_id>')
def mail_grocery_list(list_id):
    """ Email grocery list to a user """
    if not g.user:
        return abort(401)

    try:
        grocery_list = GroceryList.query.get_or_404(list_id)

        msg = Message(subject="Your Grocery List!",
                      recipients=[f"{g.user.email}"])
        msg.body = " ".join(
            [f"{ingredient.name} \n" for ingredient in grocery_list.ingredients] + [f"{ingredient} \n" for ingredient in session['ingredients']])
        msg.html = render_template(
            '/groceries/email.html', grocery_list=grocery_list)
        mail.send(msg)

        response_json = jsonify(grocery_list=grocery_list.serialize(
        ), message=f'Message sent to {g.user.email}')
        return (response_json, 200)
    except Exception as e:
        return jsonify(errors=str(e))


########################
#     Custom Errors    #
########################

# CUSTOM 404 PAGE
@ app.errorhandler(404)
def display_404(error):
    """ Displays a custom error page when returning a 404 error """
    return render_template('errors/error404.html'), 404


# CUSTOM 401 PAGE
@ app.errorhandler(401)
def display_401(error):
    """ Displays a custom error page when returning a 401 error """
    return render_template('errors/error401.html'), 401


# CUSTOM 500 PAGE
@ app.errorhandler(500)
def display_500(error):
    """ Displays a custom error page when returning a 500 error"""
    return render_template('errors/error500.html'), 500
