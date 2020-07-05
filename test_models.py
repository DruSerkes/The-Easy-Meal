# To run these tests
# Make sure FLASK_ENV=production
# python -m unittest test_models.py

from unittest import TestCase

from app import app, CURR_USER_KEY
from models import db, User, Recipe
import os

# Use test database and don't clutter tests with SQL
os.environ['DATABASE_URL'] = "postgresql:///easy_meals_test"
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


class ModelsTestcase(TestCase):
    """ Unit tests for helper functions """

    def setUp(self):
        """Make demo data."""

        self.client = app.test_client()
        User.query.delete()
        Recipe.query.delete()

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        r = Recipe(
            title="test recipe",
            image="test image path"
        )

        db.session.add_all([u, r])
        db.session.commit()
        self.u = u
        self.u_id = u.id
        self.r = r
        self.r_id = r.id
        self.email = u.email
        self.username = u.username
        self.password = u.password
        self.img_url = u.img_url
        self.is_admin = u.is_admin

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    ##########################
    #    User Model Tests    #
    ##########################

    def test_user_model(self):
        """Does basic model work?"""

        u = self.u
        # User should have no messages & no followers
        self.assertEqual(len(u.recipes), 0)
        self.assertEqual(
            u.img_url, '/static/images/icons8-kawaii-cupcake-64.png')
        self.assertEqual(u.is_admin, False)

    def test_user_repr(self):
        # User repr method
        u = self.u

        self.assertEqual(
            str(u), f'<User: {self.username}>')

    def test_user_signup(self):
        """ Test signup class method """
        # Return User instance given valid credentials
        self.assertIsInstance(User.signup({'username': 'test3', 'email': 'testing@test.com',
                                           'password': "testpwd", 'img_url': 'www.test.com/image.jpg'}), User)

        # Invalid credentials do not return User instance
        self.assertIsNot(User.signup({'username': self.username, 'email': 'testing@test.com',
                                      'password': "testpwd", 'img_url': 'www.test.com/image.jpg'}), User)

    def test_user_authenticate(self):
        """ Test authenticate class method """
        # Sign up a new user properly
        auth_u = User.signup({
            'email': "test2@test.com",
            'username': "testuser2",
            'password': "HASHED_PASSWORD2",
            'img_url': "www.test.com/test.jpg"
        }

        )

        db.session.add(auth_u)
        db.session.commit()
        # Test valid
        self.assertIsInstance(User.authenticate(
            {'username': 'testuser2', 'password': 'HASHED_PASSWORD2'}), User)
        # Test invalid username
        self.assertFalse(User.authenticate(
            {'username': 'testuserwrong', 'password': 'HASHED_PASSWORD2'}))
        # Test Invalid Password
        self.assertFalse(User.authenticate(
            {'username': 'testuser2', 'password': 'HASHED_PASSWORD_WRONG'}))

    def test_serialize_user(self):
        """ Test user serialize method """
        u = self.u
        self.assertEqual(u.serialize(), {
            'id': self.u_id,
            'username': self.username,
            'email': self.email,
            'img_url': self.img_url,
            'is_admin': self.is_admin
        })

    def test_user_recipes(self):
        # Add User 2 for relationship testing
        u = self.u
        r = self.r

        # Recipe should not be in users favorites should not
        self.assertNotIn(r, u.recipes)
        # User2 now follows User1
        u.recipes.append(r)
        db.session.commit()
        # Check if instance methods reflect change
        self.assertIn(r, u.recipes)

    ##########################
    #   Recipe Model Tests   #
    ##########################

    def test_recipe_model(self):
        """ Does basic model work? """
        r = self.r
        self.assertEqual(r.id, self.r_id)
        self.assertIsInstance(r, Recipe)
        self.assertEqual(r.title, "test recipe")
        self.assertEqual(r.image, "test image path")

    def test_new_recipe(self):
        """ Can we add messages through user-messages relationship """
        # Create new message, add to users messages
        u = self.u
        new_recipe = Recipe(title='test recipe 2', image="test recipe path 2")
        self.u.recipes.append(new_recipe)
        db.session.commit()

        self.assertEqual(len(u.recipes), 1)
        self.assertIn(new_recipe, u.recipes)
        self.assertEqual(u.recipes[0].title, new_recipe.title)
        self.assertEqual(u.recipes[0].image, new_recipe.image)
