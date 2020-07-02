""" Helper functions to keep views clean """
from secrets import student_key
from models import User, db, Recipe, Ingredient, Measurement, Step
from flask import request
import requests


API_BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
API_KEY = student_key


valid_cuisines = ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican',
                  'spanish', 'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']
valid_diets = ['pescetarian', 'lacto vegetarian',
               'ovo vegetarian', 'vegan', 'vegetarian']


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
        'x-rapidapi-key': student_key
    }


def generate_search_params(query=None, cuisine=None, diet=None, offset=0):
    """
    Returns a querystring object for recipe search
    query (str): The (natural language) recipe search query
    cuisine (str - optional): The cuisine(s) of the recipes. One or more (comma separated) of the following: african, chinese, japanese, korean, vietnamese, thai, indian, british, irish, french, italian, mexican, spanish, middle eastern, jewish, american, cajun, southern, greek, german, nordic, eastern european, caribbean, or latin american.
    diet (str - optional): The diet to which the recipes must be compliant. Possible values are: pescetarian, lacto vegetarian, ovo vegetarian, vegan, and vegetarian.
    offset (int - optional): The number of results to skip (between 0 and 900).
    """

    # valid_cuisines = ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican',
    #                   'spanish', 'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']
    # valid_diets = ['pescetarian', 'lacto vegetarian',
    #                'ovo vegetarian', 'vegan', 'vegetarian']

    # if cuisine and cuisine not in valid_cuisines:
    #     return "Invalid cuisine"
    # elif diet and diet not in valid_diets:
    #     return "Invalid diet"
    # else:
    return {
        "apiKey": student_key,
        "query": query,
        "diet": diet,
        "cuisine": cuisine,
        "offset": offset,
        "number": "12",
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
    offset = request.args.get('offset', 0)

    headers = generate_headers()
    querystring = generate_search_params(query, cuisine, diet, offset)

    print(querystring)

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
        'GET', f"{API_BASE_URL}/recipes/{id}/information", headers=headers, data={'apiKey': student_key, 'id': id})

    return response


def add_ingredients_to_db(recipe_data):
    """ 
    Add ingredients and measurements to the db
    recipe_data (obj): recipe data from the Spoonacular API with extendedIngredients - a list of ingredient objects 
    Returns a list of SQLAlchemy ingredient objects
    """
    ingredients = []
    for ingredient in recipe_data['extendedIngredients']:
        try:
            id = ingredient.get('id', None)
            name = ingredient.get('name', None)

            new_ingredient = Ingredient(id=id, name=name)
            add_and_commit(new_ingredient)

            add_measurement_for_ingredient(recipe_data, new_ingredient)

            ingredients.append(new_ingredient)
        except Exception:
            db.session.rollback()
            print(Exception)
            continue
    return ingredients


def add_measurement_for_ingredient(recipe_data, ingredient):
    """
    Add measurements for corresponding ingredients in a recipe to the db 
    recipe_data (obj): recipe data from the Spoonacular API 
    ingredient (obj): ingredient data 
    Returns the recipe from the db 
    """
    try:
        ingredient_id = ingredient.get('id', None)
        recipe_id = recipe_data.get('id', None)
        amount = i.get('amount', None)
        unit = i.get('unit', None)

        new_measurement = Measurement(
            ingredient_id=ingredient_id, recipe_id=recipe_id, amont=amount, unit=unit)
        add_and_commit(new_measurement)
    except Exception:
        db.session.rollback()
        print(Exception)

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
    # description = recipe_data.get('description', None)
    readyInMinutes = recipe_data.get('readyInMinutes', None)
    servings = recipe_data.get('servings', None)
    instructions = recipe_data.get('instructions', None)
    # TODO UPDATE TO MATCH MODEL UPDATES 

    recipe = Recipe(id=id, title=title, image=image, sourceName=sourceName, sourceUrl=sourceUrl,
                    readyInMinutes=readyInMinutes, servings=servings, instructions=instructions)
    try:
        add_and_commit(recipe)
    except Exception:
        db.session.rollback()
        print(Exception)
        return "Recipe couldn't be saved. Please try again."

    ingredients = add_ingredients_to_db(recipe_data)
    for ingredient in ingredients:
        recipe.ingredients.append(ingredient)
        db.session.commit()

    return recipe


# def add_steps_to_db(analyzed_recipe):
#     """
#     Add all the steps for a recipe to the db
#     analyzed_recipe (obj): analyzed recipe from the Spoonacular API
#     returns the analyzed_recipe
#     """
#     # TODO

# OR!!!!!
# JUST RENDER THE RECIPE.INSTRUCTIONS
# FOR AESTHETICS, HAVE SOME LOGIC THAT PARSES THE STRING AND ADDS A NEW LINE AFTER EVERY PERIOD
