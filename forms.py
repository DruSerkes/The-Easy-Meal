""" Form Models """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import InputRequired, Email, Length, Optional, EqualTo


class SignupForm(FlaskForm):
    """ User signup form  """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    email = EmailField("Email", validators=[
        InputRequired(message="Email required"), Email(message="Invalid email")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required"), EqualTo('confirm', message='Passwords must match')])

    confirm = PasswordField("Confirm Password", validators=[
                            InputRequired(message="Password confirmation required")])

    img_url = URLField('Profile Image URL (optional)', validators=[Optional()])


class LoginForm(FlaskForm):
    """ User login form """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])

# Unused feature
class GroceryListForm(FlaskForm):
    """ Form to create a new grocery list """
    title = StringField("List title", validators=[
                        InputRequired(message="Title required")])
