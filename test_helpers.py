from unittest import TestCase

from models import User, db, Recipe, Ingredient, Measurement, Step
from helpers import CURR_USER_KEY, generate_headers, generate_search_params, generate_login_data, generate_user_data
from secrets import student_key 
from forms import SignupForm, LoginForm


user = User(id=3, email="test@test.com", username="testuser", password="HASHED_PASSWORD")

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

    
        