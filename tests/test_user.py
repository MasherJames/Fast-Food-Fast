import unittest
import json
from app import create_app
from db_test import migrate, drop


class TestUser(unittest.TestCase):

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

    def test_user_signup(self):
        """ Test new user signup """
        res = self.signup()
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        """ Test for login """
        self.signup()
        res = self.login()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "You were successfully logged in Masher123")

    def test_email_exists(self):
        """ Test singing up with an existing email """
        data = {
            "username": "Simon123",
            "email": "jamesmash@gmail.com",
            "password": "Password123",
            "is_admin": 0
        }
        self.signup()

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "User with email jamesmash@gmail.com already exists")

    def test_username_exists(self):
        """ Test for existing username """
        data = {
            "username": "Masher123",
            "email": "simonkk@gmail.com",
            "password": "Password123",
            "is_admin": 0
        }
        self.signup()

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)['message'],
                         "User with username Masher123 already exists")

    def test_non_existing_user_login(self):
        """ Test non existing user login """
        data = {
            "username": "Baraka123",
            "password": "Mypassword1"
        }

        self.signup()

        res = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)['message'], "user not found")

    def test_invalid_username(self):
        """ Test invalid username on signup """
        data = {
            "username": "***1",
            "email": "nyanjui@gmail.com",
            "password": "Password123",
            "is_admin": 1
        }

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Invalid username")

    def test_invalid_email(self):
        """ Test invalid email on signup """
        data = {
            "username": "Andela12",
            "email": "andela.com",
            "password": "Password123",
            "is_admin": 1
        }

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Invalid email, enter a valid email")

    def test_invalid_password(self):
        """ Test invalid password on signup """
        data = {
            "username": "Flask123",
            "email": "flask@gmail.com",
            "password": "wrong1",
            "is_admin": 1
        }

        res = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Enter a valid password")
