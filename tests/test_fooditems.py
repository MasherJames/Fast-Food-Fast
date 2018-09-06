import unittest
import json
from app import create_app


class TestFoodItems(unittest.TestCase):

    def setUp(self):
        """ Setting up for testing """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """ Teardown the app after testing """
        self.app_context.pop()

    def signup(self):
        """ sign up function """
        signup_data = {
            "username": "Masher123",
            "email": "jamesmash@gmail.com",
            "password": "Password123",
            "is_admin": 1
        }

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(signup_data),
            headers={'content-type': 'application/json'}
        )
        return res

    def login(self):
        """ Login function """
        login_data = {
            "username": "Masher123",
            "password": "Password123"
        }

        res = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(login_data),
            headers={'content-type': 'application/json'}
        )

        return res

    def get_token(self):
        """ function to get user token """

        self.signup()
        res = self.login()
        token = json.loads(res.data).get('token', None)

        return token

    def test_user_get_token(self):
        """ Test a token is given after log in """
        self.signup()
        res = self.login()

        self.assertEqual(res.status_code, 200)
        self.assertIn('token', json.loads(res.data))

    def test_admin_create_new_fooditem(self):
        """ Test to create a new food item """
        token = self.get_token()

        data = {
            "name": "rice",
            "description": "white tasty rice",
            "price": 60
        }

        res = self.client.post(
            "api/v1/fooditems",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food item created successfully")

    def test_invalid_food_name(self):
        """ Test for invalid food name """
        token = self.get_token()

        data = {
            "name": "*******",
            "description": "white tasty ugali",
            "price": 80
        }

        res = self.client.post(
            "api/v1/fooditems",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter a valid food name")

    def test_invalid_fooditem_description(self):
        """ test to create a new food item """
        token = self.get_token()

        data = {
            "name": "chapati",
            "description": "********%%",
            "price": 120
        }

        res = self.client.post(
            "api/v1/fooditems",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter valid food description")

    def test_get_all_fooditems(self):
        """ Test to get all fooditems """
        token = self.get_token()

        res = self.client.get(
            "api/v1/fooditems",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 200)
