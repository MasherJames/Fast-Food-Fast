from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.models import FoodOrder, FoodOrders, FoodItem
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

        food_item = FoodItem().get_by_id(food_id)
        if not food_item:
            return {"message": "Food item does not exist"}, 404

        if not validators.Validators().valid_inputs(destination):
            return {"message": "Enter a valid destination"}, 400

        food_order = FoodOrder(food_item.name, destination)
        FoodOrders.append(food_order)

        return {"message": "Food order placed succssesfully"}, 201


class GetOrders(Resource):

    @jwt_required
    def get(self):
        """ get all the orders """
        return{"Food orders": [food_order.serialize() for food_order in FoodOrders]}, 200
