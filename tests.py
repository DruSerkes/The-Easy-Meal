from unittest import TestCase

from app import app
from models import db, User, Recipe,

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///easy_meals_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

USER_DATA = {
    'username': 'TEST USER',
    'password': 'TEST PASSWORD',
    'email': 'test@test.com',
}


class HelpersTestcase(TestCase):
    """ Unit tests for helper functions """

    def setUp(self):
        """Make demo data."""

        User.query.delete()

        user = User(**USER_DATA)
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
