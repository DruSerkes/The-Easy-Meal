from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, BooleanField, EmailField, URLField
from wtforms.validators import InputRequired, Email, Length, Optional


# THESE STILL NEED WORK - I JUST COPY/PASTED THESE SO I KNOW WHERE TO START
class SignupForm(FlaskForm):
    """ User signup form  """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    email = StringField("Email", validators=[
        InputRequired(message="Email required"), Email()])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])

    img_url = URLField('Profile Image URL (optional)', validators=[Optional()])


class LoginForm(FlaskForm):
    """ User login form """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])


class GroceryListForm(FlaskForm):
    """ Form to create a new grocery list """
    title = StringField("List title", validators=[
                        InputRequired(message="Title required")])
