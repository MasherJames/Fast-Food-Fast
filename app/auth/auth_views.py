import datetime
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from models.models import User
from utils import validators


class SignUp(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        """ SignUp a new user """
        request_data = SignUp.parser.parse_args()

        username = request_data['username']
        email = request_data['email']
        password = request_data['password']

        if not validators.Validators().valid_username(username):
            return {"message": "Invalid username"}, 400

        if not validators.Validators().valid_email(email):
            return {"message": "Invalid email, enter a valid email"}, 400

        if not validators.Validators().valid_password(password):
            return {"message": "Enter a valid password"}, 400

        if User().get_by_username(username):
            return {"message": f"User with username {username} already exists"}, 400

        if User().get_by_email(email):
            return {"message": f"User with email {email} already exists"}, 400

        user = User(username, email, password)

        user.add()

        return {"message": f"Account for {username} has been created successfully"}, 201


class Login(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        """ Log in a signed up user """
        request_data = Login.parser.parse_args()

        username = request_data['username']
        password = request_data['password']

        user = User().get_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            expires = datetime.timedelta(minutes=30)
            token = create_access_token(
                user.username, expires_delta=expires)
            return {'token': token, 'message': f'You were successfully logged in {username}'}, 200
        return {'message': 'user not found'}, 404
