""" Helper functions to keep views clean """


def generate_user_data(form):
    """
    Access form for user data 
    Returns a user_data object 
    """
    username = form.username.data
    password = form.password.data
    email = form.email.data
    img_url = form.img_url.data
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
