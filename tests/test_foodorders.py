import unittest
import json
from app import create_app
from migrate import TablesSetup


class TestFoodOrders(unittest.TestCase):

    def setUp(self):
        """ Setting up for testing """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
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

    def test_customer_post_order(self):
        """ Test for a customer to create an order for a food item """
        token = self.get_token()

        data = {
            "destination": "juja"
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order placed succssesfully")

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

    def test_invalid_destination(self):
        """ Test for an invalid destination """
        token = self.get_token()

        data = {
            "destination": "********"
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter a valid destination")

    def test_get_all_orders(self):
        """ Test get all orders """
        token = self.get_token()

        res = self.client.get(
            "api/v1/fooditems/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 200)

    def test_get_specific_orders(self):
        """ Get a specific food order"""
        token = self.get_token()

        res = self.client.get(
            "api/v1/fooditems/orders/1",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 200)

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

    def test_update_the_status_of_an_order(self):
        """ Test update food order status """
        token = self.get_token()

        res = self.client.put(
            "api/v1/fooditems/orders/1",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 200)
