from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


# THESE STILL NEED WORK - I JUST COPY/PASTED THESE SO I KNOW WHERE TO START
class RegisterForm(FlaskForm):
    """ Registration form  """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])

    email = StringField("Email", validators=[
        InputRequired(message="Email required"), Email()])

    first_name = StringField("First Name", validators=[
        InputRequired(message="First name required")])

    last_name = StringField("Last Name", validators=[
        InputRequired(message="Last name required")])


class LoginForm(FlaskForm):
    """ User login form """
    username = StringField("Username", validators=[
        InputRequired(message="Username required")])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password required")])
