from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.models import FoodOrder, FoodItem
from utils import validators


class PostOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('destination', type=str, required=True,
                        help='This field cannot be left blank')

    @jwt_required
    def post(self, food_id):
        """ Place an order for a specific food item"""
        request_data = PostOrders.parser.parse_args()

        destination = request_data['destination']

        current_user = get_jwt_identity()

        food_item = FoodItem().get_by_id(food_id)
        if not food_item:
            return {"message": "Food item does not exist"}, 404

        if not validators.Validators().valid_inputs(destination):
            return {"message": "Enter a valid destination"}, 400

        food_order = FoodOrder(current_user, food_item.name, destination)

        food_order.add()

        return {"message": "Food order placed succssesfully"}, 201


class GetOrders(Resource):

    @jwt_required
    def get(self):
        """ Fetch all the orders """
        FoodOrders = FoodOrder().get_all()

        if FoodOrders is None:
            return {"Message": "There are no available food orders now"}, 404
        return{"Food orders": [food_order.serialize() for food_order in FoodOrders]}, 200


class SpecificCustomerOrders(Resource):

    @jwt_required
    def get(self):
        """ Customer can fetch all orders under his username """
        current_user = get_jwt_identity()

        customer_orders = FoodOrder().get_by_requester(current_user)

        if customer_orders:
            return {"Food orders": [customer_order.serialize() for customer_order in customer_orders]}, 200

        return {"Message": "You don't have any orders"}, 404
