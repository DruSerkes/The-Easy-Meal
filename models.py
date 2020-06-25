""" SQLAlchemy Models for Easy Meal """

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """ Connect to Database """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Model """
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    img_url = db.Column(
        db.String, default='/static/images/icons8-kawaii-cupcake-64.png')
    is_admin = db.Column(db.Boolean, default=False)
    recipes = db.relationship('Recipe', backref='users')

    @classmethod
    def register(cls, data):
        """ Generate hashed password and register a new user """
        hashed = bcrypt.generate_password_hash(data['password'])
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=data['username'], password=hashed_utf8, email=data['email'], first_name=data['first_name'], last_name=data['last_name'])

    @classmethod
    def authenticate(cls, data):
        """ Validate user exists & pwd is correct

        return user if valid; else return False
        """

        u = User.query.filter_by(username=data['username']).first()
        if u and bcrypt.check_password_hash(u.password, data['password']):
            return u
        else:
            return False

    def get_full_name(self):
        """ Returns first and last name together """
        return f'{self.first_name} {self.last_name}'
