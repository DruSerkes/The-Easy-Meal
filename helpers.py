""" Helper functions to keep views clean """
from models import User, db
from secrets import student_key


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


def generate_search_params(query, cuisine=None, diet=None, offset=0):
    """ 
    Returns a querystring object for recipe search
    query (str): The (natural language) recipe search query
    cuisine (str - optional): The cuisine(s) of the recipes. One or more (comma separated) of the following: african, chinese, japanese, korean, vietnamese, thai, indian, british, irish, french, italian, mexican, spanish, middle eastern, jewish, american, cajun, southern, greek, german, nordic, eastern european, caribbean, or latin american.
    diet (str - optional): The diet to which the recipes must be compliant. Possible values are: pescetarian, lacto vegetarian, ovo vegetarian, vegan, and vegetarian.
    offset (int - optional): The number of results to skip (between 0 and 900).
    """
    if not query or not isinstance(query, str):
        return "Invalid or missing query"

    valid_cuisines = ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican',
                      'spanish', 'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']
    valid_diets = ['pescetarian', 'lacto vegetarian',
                   'ovo vegetarian', 'vegan', 'vegetarian']

    if cuisine and cuisine.lower() not in valid_cuisines:
        return "Invalid cuisine"
    elif diet and diet.lower() not in valid_diets:
        return "Invalid diet"
    else:
        return {
            "query": query,
            "diet": diet.lower(),
            "cuisine": cuisine.lower(),
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
