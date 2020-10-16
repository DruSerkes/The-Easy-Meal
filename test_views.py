# To run these tests:
# FLASK_ENV=production
# python -m unittest test_views.py

from unittest import TestCase

from app import app, CURR_USER_KEY
from models import db, connect_db, Recipe, User, GroceryList
import os
from forms import SignupForm, LoginForm
from flask import Flask

connect_db(app)

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///easy_meals_test"
app.config['SQLALCHEMY_ECHO'] = False

# Now we can import app

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class ViewsTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        Recipe.query.delete()
        GroceryList.query.delete()
        User.query.delete()

        u = User.signup({
            'email': "test@test.com",
            'username': "testuser",
            'password': "HASHED_PASSWORD",
            'img_url': "www.test.com/test.jpg"}
        )
        r = Recipe(
            title="test recipe",
            image="test image path"
        )

        db.session.add_all([u, r])
        db.session.commit()
        g = GroceryList(user_id=u.id)
        db.session.add(g)
        db.session.commit()

        self.u = u
        self.u_id = u.id
        self.r = r
        self.r_id = r.id
        self.g = g
        self.g_id = g.id
        self.email = u.email
        self.username = u.username
        self.img_url = u.img_url

    def tearDown(self):
        """ Clean up any fouled transactions """
        db.session.rollback()

    def test_signup_page(self):
        """ Test signup """
        with self.client as c:
            resp = c.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('</form>', html)

    # def test_signup_new_user(self):
    #     """ Test new user signup """
    #     with app.app_context():
    #         with self.client as c:
    #             new_user = User(username='newuser', password='newpwd',
    #                             email='new@test.com', img_url='test.com/img.jpg')
    #             form = SignupForm(obj=new_user)

    #             resp = c.post(
    #                 '/signup', data=form, follow_redirects=True)
    #             html = resp.get_data(as_text=True)

    #             user = User.query.filter(User.username == 'newuser').first()

    #             self.assertEqual(resp.status_code, 200)
    #             self.assertIn(user.img_url, html)
    #             self.assertIn('Easy Meals', html)
    #             self.assertIn("Lets get cookin!", html)

    def test_login_user_form(self):
        """ Test user login form """
        with self.client as c:
            resp = c.get('/login')
            html = resp.get_data(as_text=True)
            # check resp before login
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', html)
            self.assertIn('</form>', html)

    # def test_login_user(self):
    #     """ Test user login """
    #     with app.app_context():
    #         with self.client as c:
    #             form = LoginForm()
    #             resp = c.post('/login', data={form.username.data: 'testuser',
    #                                           form.password.data: 'HASHED_PASSWORD'}, follow_redirects=True)
    #             user = User.query.filter(User.username == 'testuser').first()
    #             html = resp.get_data(as_text=True)

    #             self.assertEqual(resp.status_code, 200)
    #             self.assertIn(self.img_url, html)
    #             self.assertIn(self.username, html)
    #             self.assertIn('Easy Meals', html)
    #             self.assertIn("Lets get cookin!", html)

    def test_logout_user(self):
        """ Test user logout """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u_id
            resp = c.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.img_url, html)
            self.assertIn('You have been logged out', html)
            self.assertNotIn(self.u_id, sess)

    # def test_favorite_recipe(self):
    #     """Can use favorite a recipe?"""

    #     # Since we need to change the session to mimic logging in,
    #     # we need to use the changing-session trick:

    #     with self.client as c:
    #         with c.session_transaction() as session:
    #             session[CURR_USER_KEY] = self.u_id

    #         # Now, that session setting is saved, so we can have
    #         # the rest of ours test

    #         resp = c.post(url_for(), data={"text": "Hello"})

    #         # Make sure it redirects
    #         self.assertEqual(resp.status_code, 302)

    #         msg = Message.query.one()
    #         self.assertEqual(msg.text, "Hello")
    #         self.assertEqual(msg.user_id, self.testuser.id)
