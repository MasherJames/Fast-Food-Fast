import unittest
import json
from app import create_app
from db_test import migrate, drop


class TestFoodItems(unittest.TestCase):

    def setUp(self):
        """ Setting up for testing """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            drop()
            migrate()

    def signup(self):
        """ sign up function """
        signup_data = {
            "username": "Masher123",
            "email": "masher@gmail.com",
            "password": "Password123"
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

    def test_non_admin_create_fooditem(self):
        """ Test non admin create a new food item """
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

        self.assertEqual(res.status_code, 401)
        self.assertEqual(json.loads(res.data)[
                         'message'], 'Your cannot access this level')

    def test_fooditem_does_not_exist(self):
        """ Test food item does not exist """
        token = self.get_token()

        data = {
            "destination": "juja"
        }

        res = self.client.post(
            "/api/v1/fooditems/100/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food item does not exist")

    def test_food_order_does_not_exist(self):
        """ Test food order does not exist """
        token = self.get_token()

        res = self.client.get(
            "api/v1/fooditems/orders/100",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order does not exist")
