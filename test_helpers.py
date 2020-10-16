from unittest import TestCase

from models import User, db, Recipe, Ingredient, Measurement, Step
from helpers import CURR_USER_KEY, generate_headers, generate_search_params, generate_login_data, generate_user_data
from secrets import student_key


class TestData():
    def __init__(self, data):
        self.data = data


class TestForm():
    def __init__(self, username, password, email, img_url):
        self.username = username
        self.password = password
        self.email = email
        self.img_url = img_url


form = TestForm(username=TestData("test"), password=TestData(
    "testword"), email=TestData("test@test.com"), img_url=TestData("test_url"))


class HelpersTestCase(TestCase):
    """ Unit tests for helper functions """

    def test_generate_headers(self):
        """ generate_headers tests """
        self.assertIsInstance(generate_headers(), object)
        self.assertEqual(generate_headers(), {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': student_key
        })

    def test_generate_search_params(self):
        """ generate_headers tests """
        self.assertIsInstance(generate_search_params("test"), object)
        self.assertEqual(generate_search_params("test", "testly"), {
            "apiKey": student_key,
            "query": 'test',
            "diet": None,
            "cuisine": "testly",
            "offset": 0,
            "number": 12
        })

    def test_generate_user_data(self):
        """ generate_user_data tests """
        self.assertIsInstance(generate_user_data(form), object)
        self.assertEqual(generate_user_data(form), {
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data,
            'img_url': form.img_url.data
        })

    def test_generate_login_data(self):
        """ generate_user_data tests """
        self.assertIsInstance(generate_login_data(form), object)
        self.assertEqual(generate_login_data(form), {
            'username': form.username.data,
            'password': form.password.data,
        })
