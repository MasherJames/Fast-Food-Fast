from functools import wraps
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import FoodItem, FoodOrder, User
from utils import validators


def admin_access(f):
    ''' Restrict access if not admin '''
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        user = User().get_by_username(get_jwt_identity())
        if not user.is_admin:
            return {'message': 'Your cannot access this level'}, 401
        return f(*args, **kwargs)

    return wrapper_function


class Foods(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('description', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('price', type=int, required=True,
                        help='This field cannot be left blank')

    @jwt_required
    @admin_access
    def post(self):
        """ Create a new food item """
        request_data = Foods.parser.parse_args()

        name = request_data['name']
        description = request_data['description']
        price = request_data['price']

        if not validators.Validators().valid_inputs(name):
            return {"message": "Enter a valid food name"}, 400

        if not validators.Validators().valid_inputs(description):
            return {"message": "Enter valid food description"}, 400

        food_item = FoodItem(name, description, price)

        food_item.add()

        return {"message": "Food item created successfully"}, 201

    @jwt_required
    def get(self):
        """ Get all food items """
        FoodItems = FoodItem().get_all()
        if FoodItems:
            return {"Food Items": [food_item.serialize() for food_item in FoodItems]}, 200
        return {"message": "No food items available for now"}, 404


class SpecificItem(Resource):

    @jwt_required
    def get(self, food_item_id):
        """ Get a specific item """

        food_item = FoodItem().get_by_id(food_item_id)

        if food_item:
            return food_item.serialize(), 200

        return {"Message": "Food item does not exist"}, 404

    @jwt_required
    @admin_access
    def delete(self, food_item_id):
        """ Admin can delete a specific food item """
        food_item = FoodItem().get_by_id(food_item_id)

        if food_item:
            food_item.delete(food_item_id)
            return {"message": "Food item deleted successfully"}, 200

        return {"message": "Food item does not exist"}, 404

    @jwt_required
    @admin_access
    def put(self, food_item_id):
        """ Update an existing food item """
        request_data = Foods.parser.parse_args()

        name = request_data['name']
        description = request_data['description']
        price = request_data['price']

        if not validators.Validators().valid_inputs(name):
            return {"message": "Invalid food name"}, 400

        if not validators.Validators().valid_inputs(description):
            return {"message": "Invalid food description"}, 400

        if FoodItem().get_by_id(food_item_id):
            updated_food_item = FoodItem(name, description, price)
            updated_food_item.update(food_item_id)
            return {"message": "Food item updated successfully"}, 200

        return {"message": "Food item does not exist"}, 404


class SpecificOrder(Resource):

    @jwt_required
    def get(self, food_order_id):
        """ Fetch a specific order """
        food_order = FoodOrder().get_by_id(food_order_id)

        if not food_order:
            return {"message": "Food order does not exist"}, 404

        return food_order.serialize(), 200


class AcceptOrder(Resource):

    @jwt_required
    @admin_access
    def put(self, food_order_id):
        """ Update the status of an order to accepted """

        food_order = FoodOrder().get_by_id(food_order_id)

        if not food_order:
            return {"message": "Food order does not exist"}, 404

        if food_order.status != "pending":
            return {"message": f"Food order already {food_order.status}"}, 403

        food_order.accept_order(food_order_id)
        return {"Message": "Food order accepted"}, 200


class AcceptedOrders(Resource):
    @jwt_required
    @admin_access
    def get(self):
        ''' Get all accepted orders '''
        accepted_orders = FoodOrder().get_accepted_orders()

        if accepted_orders:
            return {"Accepted Orders": [accepted_order.serialize() for accepted_order in accepted_orders]}, 200
        return {"message": "there are no accepted orders now"}, 404


class DeclineOrder(Resource):

    @jwt_required
    @admin_access
    def put(self, food_order_id):
        """ Update the status of an order to declined """

        food_order = FoodOrder().get_by_id(food_order_id)

        if not food_order:
            return {"message": "Food order does not exist"}, 404

        if food_order.status != "pending":
            return {"message": f"Food order already {food_order.status}"}, 403

        food_order.decline_order(food_order_id)
        return {"Message": "Food order declined"}, 200


class DeclinedOrders(Resource):
    @jwt_required
    @admin_access
    def get(self):
        ''' Get all declined orders '''
        declined_orders = FoodOrder().get_declined_orders()

        if declined_orders:
            return {"Declined Orders": [declined_order.serialize() for declined_order in declined_orders]}, 200
        return {"message": "there are no declined orders now"}, 404


class CompleteOrder(Resource):

    @jwt_required
    @admin_access
    def put(self, food_order_id):
        """ Update the status of an order to completed if it was accepted """

        food_order = FoodOrder().get_by_id(food_order_id)

        if not food_order:
            return {"message": "Food order does not exist"}, 404

        if food_order.status != "accepted":
            return {"message": f"You cannot complete this order, it is already {food_order.status}"}, 403

        food_order.complete_accepted_order(food_order_id)
        return {"Message": "Food order completed"}, 200


class CompletedOrders(Resource):
    @jwt_required
    @admin_access
    def get(self):
        ''' Get all completed orders '''
        complete_orders = FoodOrder().get_completed_orders()

        if complete_orders:
            return {"Complete Orders": [complete_order.serialize() for complete_order in complete_orders]}, 200
        return {"message": "there are no complete orders now"}, 404
