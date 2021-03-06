""" Helper functions to keep views clean """
# COMMENT OUT THIS LINE FOR PRODUCTION
# from secrets import student_key
from models import User, db, Recipe, Ingredient, Measurement, Step
from flask import request, session
import requests
import os


CURR_USER_KEY = "user_id"
API_BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"

# COMMENT THIS LINE OUT FOR PRODUCTION
# API_KEY = os.environ.get('student_key', student_key)

# USE THIS LINE FOR PRODUCTION
API_KEY = os.environ['student_key']


valid_cuisines = ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican',
                  'spanish', 'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']
valid_diets = ['pescetarian', 'lacto vegetarian',
               'ovo vegetarian', 'vegan', 'vegetarian']


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def generate_user_data(form):
    """
    Access form for user data
    Returns a user_data object
    """
    username = form.username.data
    password = form.password.data
    email = form.email.data
    img_url = form.img_url.data or User.img_url.default.arg
    return {
        'username': username,
        'password': password,
        'email': email,
        'img_url': img_url
    }


def generate_login_data(form):
    """
    Access form data for user login credentials
    Returns a login_data object
    """
    username = form.username.data
    password = form.password.data

    return {
        "username": username,
        "password": password
    }


def generate_headers():
    """ Returns headers """
    return {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }


def generate_search_params(query=None, cuisine=None, diet=None, offset=0, number=12):
    """
    Returns a querystring object for recipe search
    query (str): The (natural language) recipe search query
    cuisine (str - optional): The cuisine(s) of the recipes. One or more (comma separated) of the following: african, chinese, japanese, korean, vietnamese, thai, indian, british, irish, french, italian, mexican, spanish, middle eastern, jewish, american, cajun, southern, greek, german, nordic, eastern european, caribbean, or latin american.
    diet (str - optional): The diet to which the recipes must be compliant. Possible values are: pescetarian, lacto vegetarian, ovo vegetarian, vegan, and vegetarian.
    offset (int - optional): The number of results to skip (between 0 and 900).
    """

    return {
        "apiKey": API_KEY,
        "query": query,
        "diet": diet,
        "cuisine": cuisine,
        "offset": offset,
        "number": number
    }


def add_and_commit(obj):
    """
    Add and commit an obj to the db
    Returns obj
    """
    db.session.add(obj)
    db.session.commit()
    return obj


def do_search(request):
    """
    Get recipes from user request from Spoonacular API
    Returns a response
    """
    query = request.args.get('query', "")
    cuisine = request.args.get('cuisine', "")
    diet = request.args.get('diet', "")
    offset = int(request.args.get('offset', 0))

    headers = generate_headers()
    querystring = generate_search_params(query, cuisine, diet, offset)

    response = requests.request(
        "GET", f"{API_BASE_URL}/recipes/search", headers=headers, params=querystring)

    return response


def get_recipe(id):
    """
    Get recipe information from API
    Returns a recipe object
    """
    headers = generate_headers()
    response = requests.request(
        'GET', f"{API_BASE_URL}/recipes/{id}/information", headers=headers, data={'apiKey': API_KEY, 'id': id})

    return response


def add_ingredients_to_db(recipe_data):
    """ 
    Add ingredients and measurements to the db
    recipe_data (obj): recipe data from the Spoonacular API with extendedIngredients - a list of ingredient objects 
    Returns a list of SQLAlchemy ingredient objects
    """
    ingredient_list = []
    for ingredient in recipe_data['extendedIngredients']:
        try:
            db_ingredient = Ingredient.query.filter_by(
                id=ingredient['id']).first()
            if db_ingredient:
                ingredient_list.append(db_ingredient)
            else:
                id = ingredient.get('id', None)
                name = ingredient.get('name', None)
                original = ingredient.get('original', None)

                new_ingredient = Ingredient(
                    id=id, name=name, original=original)

                new_ingredient = add_and_commit(new_ingredient)
                print(f"\n Created new ingredient {new_ingredient} \n")

                ingredient_list.append(new_ingredient)
                print(f"\n Ingredient added to list: {ingredient_list} \n")

                recipe_data = add_measurement_for_ingredient(
                    ingredient, recipe_data)

        except Exception as e:
            print(str(e))
            # import pdb
            # pdb.set_trace()
            db.session.rollback()
            continue
    return ingredient_list


def add_measurement_for_ingredient(ingredient, recipe_data):
    """
    Add measurements for corresponding ingredients in a recipe to the db 
    recipe_data (obj): recipe data from the Spoonacular API 
    ingredient (obj): ingredient data 
    Returns the recipe from the db 
    """
    try:
        recipe_id = recipe_data.get('id', None)
        ingredient_id = ingredient.get('id', None)
        amount = ingredient.get('amount', None)
        unit = ingredient.get('unit', None)
        new_measurement = Measurement(
            ingredient_id=ingredient_id, recipe_id=recipe_id, amount=amount, unit=unit)
        new_measurement = add_and_commit(new_measurement)

    except Exception as e:
        db.session.rollback()
        # import pdb
        # pdb.set_trace()
        print('***********************')
        print(str(e))
        print('***********************')

    return recipe_data


def add_recipe_to_db(recipe_data):
    """
    Add a recipe to the db
    recipe_data (obj): recipe data from the Spoonacular API
    Returns the recipe from the db
    """
    id = recipe_data.get('id', None)
    title = recipe_data.get('title', None)
    image = recipe_data.get('image', None)
    sourceName = recipe_data.get('sourceName', None)
    sourceUrl = recipe_data.get('sourceUrl', None)
    readyInMinutes = recipe_data.get('readyInMinutes', None)
    servings = recipe_data.get('servings', None)
    instructions = recipe_data.get('instructions', None)
    vegetarian = recipe_data.get('vegetarian', None)
    vegan = recipe_data.get('vegan', None)
    glutenFree = recipe_data.get('glutenFree', None)
    dairyFree = recipe_data.get('dairyFree', None)
    sustainable = recipe_data.get('sustainable', None)
    ketogenic = recipe_data.get('ketogenic', None)
    whole30 = recipe_data.get('whole30', None)

    recipe = Recipe(id=id, title=title, image=image, sourceName=sourceName, sourceUrl=sourceUrl,
                    readyInMinutes=readyInMinutes, servings=servings, instructions=instructions, vegetarian=vegetarian, vegan=vegan, glutenFree=glutenFree, dairyFree=dairyFree, sustainable=sustainable, ketogenic=ketogenic, whole30=whole30)
    try:
        recipe = add_and_commit(recipe)
    except Exception:
        # import pdb
        # pdb.set_trace()
        db.session.rollback()
        print(str(Exception))
        return "Recipe couldn't be saved. Please try again."

    ingredients = add_ingredients_to_db(recipe_data)
    for ingredient in ingredients:
        recipe.ingredients.append(ingredient)
        db.session.commit()

    return recipe
