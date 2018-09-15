import unittest
import json
from datetime import datetime
from app import create_app
from db_test import migrate, drop


class TestFoodItems(unittest.TestCase):

    def setUp(self):
        """ Setting up for testing """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.data = {
            'food_item_data': {
                "name": "chapati",
                "description": "sweet chapati",
                "price": 40
            }
        }
        with self.app.app_context():
            drop()
            migrate()

    def signup_admin(self):
        """ sign up function """
        signup_data = {
            "username": "AdminUser",
            "email": "admin@gmail.com",
            "password": "Adminpass123",
            "is_admin": True
        }

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(signup_data),
            headers={'content-type': 'application/json'}
        )
        return res

    def login_admim(self):
        """ Login function """
        login_data = {
            "username": "AdminUser",
            "password": "Adminpass123"
        }

        res = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(login_data),
            headers={'content-type': 'application/json'}
        )

        return res

    def get_admin_token(self):
        """ function to get user token """

        self.signup_admin()
        res = self.login_admim()
        token = json.loads(res.data).get('token', None)

        return token

    def post_food_item(self, token):
        """ post a new food item """
        res = self.client.post(
            "/api/v1/fooditems",
            data=json.dumps(self.data['food_item_data']),
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        return res

    def test_admin_signup(self):
        """ Test for successfully admin sign up """
        res = self.signup_admin()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Account for AdminUser has been created successfully")

    def test_admin_login(self):
        """ Test for admin has logged in """
        self.signup_admin()
        res = self.login_admim()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "You were successfully logged in AdminUser")

    def test_admin_user_get_token(self):
        """ Test a token is given after log in """
        self.signup_admin()
        res = self.login_admim()

        self.assertEqual(res.status_code, 200)
        self.assertIn('token', json.loads(res.data))

    def test_admin_can_post_fooditem(self):
        """ Test admin can add a food item """
        admin_token = self.get_admin_token()

        res = self.post_food_item(admin_token)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], 'Food item created successfully')

    def test_invalid_food_name_fooditem(self):
        """ Test admin can add a food item """
        admin_token = self.get_admin_token()

        data = {
            "name": "****",
            "description": "sweet invalid food",
            "price": 50
        }

        res = self.client.post(
            "/api/v1/fooditems",
            data=json.dumps(data),
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        print(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter a valid food name")

    def test_invalid_food_description_fooditem(self):
        """ Test admin can add a food item """
        admin_token = self.get_admin_token()

        data = {
            "name": "Ugali ugali",
            "description": "*****",
            "price": 50
        }

        res = self.client.post(
            "/api/v1/fooditems",
            data=json.dumps(data),
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter valid food description")

    def test_admin_get_all_fooditems(self):
        """ Test admin to get all food items """

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        res = self.client.get(
            "/api/v1/fooditems",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_empty_fooditems(self):
        """ Test empty fooditems """

        admin_token = self.get_admin_token()

        res = self.client.get(
            "/api/v1/fooditems",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "No food items available for now")

    def test_admin_get_single_fooditem(self):
        """ Test admin to get single food item """

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        res = self.client.get(
            "/api/v1/fooditems/1",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 200)

    def test_get_non_existing_fooditem(self):
        """ Test get non existing food item """

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        res = self.client.get(
            "/api/v1/fooditems/11234567",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'Message'], "Food item does not exist")

    def test_delete_existing_fooditem(self):
        """ Test delete food item"""

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        res = self.client.delete(
            "/api/v1/fooditems/1",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food item deleted successfully")

    def test_delete_non_existing_fooditem(self):
        """ Test delete non existing food item"""

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        res = self.client.delete(
            "/api/v1/fooditems/10000",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food item does not exist")

    def test_update_existing_fooditem(self):
        """ Test update food item """

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        update_data = {
            "name": "update name",
            "description": "updated description",
            "price": 35
        }

        res = self.client.put(
            "/api/v1/fooditems/1",
            data=json.dumps(update_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food item updated successfully")

    def test_update_existing_fooditem_with_invalid_name(self):
        """ Test update food item with invalid name"""

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        update_data = {
            "name": "******",
            "description": "updated description",
            "price": 35
        }

        res = self.client.put(
            "/api/v1/fooditems/1",
            data=json.dumps(update_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Invalid food name")

    def test_update_existing_fooditem_with_invalid_description(self):
        """ Test update food item with invalid name"""

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        update_data = {
            "name": "valid name",
            "description": "****",
            "price": 35
        }

        res = self.client.put(
            "/api/v1/fooditems/1",
            data=json.dumps(update_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Invalid food description")

    def test_update_non_existing_fooditem(self):
        """ Test update non existing food item """

        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        update_data = {
            "name": "update name",
            "description": "updated description",
            "price": 35
        }

        res = self.client.put(
            "/api/v1/fooditems/10000",
            data=json.dumps(update_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'],  "Food item does not exist")

    def post_order_to_fooditem(self):
        """ Post order to fooditem """
        admin_token = self.get_admin_token()
        self.post_food_item(admin_token)

        order_data = {
            "destination": "thika"
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(order_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )

        return res

    def test_post_order_to_existing_fooditem(self):
        """ Test Post order to a specific food item """
        res = self.post_order_to_fooditem()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order placed succssesfully")

    def test_post_order_to_non_existing_fooditem(self):
        """ Post order to a non existing food item """
        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        order_data = {
            "destination": "thika"
        }

        res = self.client.post(
            "/api/v1/fooditems/4000/orders",
            data=json.dumps(order_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food item does not exist")

    def test_post_order_with_invalid_destination(self):
        """ Post order with invalid destination"""
        admin_token = self.get_admin_token()

        self.post_food_item(admin_token)

        order_data = {
            "destination": "*****"
        }

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(order_data),
            headers={
                'Authorization': f'Bearer {admin_token}',
                'content-type': 'application/json'
            }
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter a valid destination")

    def test_get_all_orders(self):
        """ Test get all food orders """
        admin_token = self.get_admin_token()
        self.post_order_to_fooditem()

        res = self.client.get(
            "/api/v1/fooditems/orders",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 200)

    def test_get_non_existing_orders(self):
        """ Test get non existing orders """
        admin_token = self.get_admin_token()

        res = self.client.get(
            "/api/v1/fooditems/orders",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'Message'], "There are no available food orders now")

    def test_get_orders_by_customername(self):
        """ Test get all food orders for a specific customer """
        admin_token = self.get_admin_token()
        self.post_order_to_fooditem()

        res = self.client.get(
            "/api/v1/fooditems/orders/customer_name",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 200)

    def test_non_existing_orders_by_customername(self):
        """ Test get non existing food orders for a specific customer """
        admin_token = self.get_admin_token()

        res = self.client.get(
            "/api/v1/fooditems/orders/customer_name",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'Message'], "You don't have any orders")

    def accept_order(self):
        """  accept an order """
        admin_token = self.get_admin_token()

        self.post_order_to_fooditem()

        res = self.client.put(
            "/api/v1/fooditems/orders/1/accept",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        return res

    def test_admin_accept_order(self):
        """ Test for admin to accept an order """
        res = self.accept_order()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'Message'], "Food order accepted")

    def test_accept_accepted_order(self):
        """ Test accepted order """
        self.accept_order()
        res = self.accept_order()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order already accepted")

    def test_accept_non_existing_order(self):
        """ Test accept non existing order """
        admin_token = self.get_admin_token()

        res = self.client.put(
            "/api/v1/fooditems/orders/1/accept",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order does not exist")

    def test_get_all_accepted_orders(self):
        """Test Get all accepted orders """
        admin_token = self.get_admin_token()
        self.accept_order()

        res = self.client.get(
            "/api/v1/fooditems/orders/accepted",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_non_existing_accepted_orders(self):
        """ Test non existing accepted orders """
        admin_token = self.get_admin_token()

        res = self.client.get(
            "/api/v1/fooditems/orders/accepted",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "there are no accepted orders now")

    def decline_order(self):
        """ Decline an order """
        admin_token = self.get_admin_token()

        self.post_order_to_fooditem()

        res = self.client.put(
            "/api/v1/fooditems/orders/1/decline",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        return res

    def test_admin_decline_order(self):
        """ Test for admin to decline an order """
        res = self.decline_order()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'Message'], "Food order declined")

    def test_decline_declined_order(self):
        """ Test already declined order """
        self.decline_order()
        res = self.decline_order()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order already declined")

    def test_decline_non_existing_order(self):
        """ Test decline non existing order """
        admin_token = self.get_admin_token()

        res = self.client.put(
            "/api/v1/fooditems/orders/1/decline",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order does not exist")

    def test_get_all_declined_orders(self):
        """Test Get all declined orders """
        admin_token = self.get_admin_token()
        self.decline_order()

        res = self.client.get(
            "/api/v1/fooditems/orders/declined",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_non_existing_declined_orders(self):
        """ Test non existing declined orders """
        admin_token = self.get_admin_token()

        res = self.client.get(
            "/api/v1/fooditems/orders/declined",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "there are no declined orders now")

    def complete_order(self):
        """ Complete accepted order """
        admin_token = self.get_admin_token()

        self.post_order_to_fooditem()

        self.client.put(
            "/api/v1/fooditems/orders/1/accept",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        res = self.client.put(
            "/api/v1/fooditems/orders/1/complete",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        return res

    def test_admin_complete_order(self):
        """ Test for admin to complete an order """
        res = self.complete_order()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'Message'], "Food order completed")

    def test_complete_completed_order(self):
        """ Test already completed order """
        self.complete_order()
        res = self.complete_order()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(json.loads(res.data)[
                         'message'], "You cannot complete this order, it is already completed")

    def test_complete_non_existing_order(self):
        """ Test complete non existing order """
        admin_token = self.get_admin_token()

        res = self.client.put(
            "/api/v1/fooditems/orders/1/complete",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Food order does not exist")

    def test_get_all_completed_orders(self):
        """Test Get all completed orders """
        admin_token = self.get_admin_token()
        self.complete_order()

        res = self.client.get(
            "/api/v1/fooditems/orders/completed",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_non_existing_completed_orders(self):
        """ Test non existing completed orders """
        admin_token = self.get_admin_token()

        res = self.client.get(
            "/api/v1/fooditems/orders/completed",
            headers={
                'Authorization': f'Bearer {admin_token}'
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "there are no complete orders now")
