from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, BooleanField, EmailField, URLField
from wtforms.validators import InputRequired, Email, Length, Optional


# THESE STILL NEED WORK - I JUST COPY/PASTED THESE SO I KNOW WHERE TO START
class SignUpForm(FlaskForm):
    """ Registration form  """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])

    email = StringField("Email", validators=[
        InputRequired(message="Email required"), Email()])

    img_url = Url


class LoginForm(FlaskForm):
    """ User login form """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])
