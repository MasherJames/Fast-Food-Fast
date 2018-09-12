from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.models import FoodItem, FoodOrder
from utils import validators


class Foods(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('description', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('price', type=int, required=True,
                        help='This field cannot be left blank')

    @jwt_required
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
    def delete(self, food_item_id):
        """ Admin can delete a specific food item """
        food_item = FoodItem().get_by_id(food_item_id)

        if food_item:
            food_item.delete(food_item_id)
            return {"message": "Food item deleted successfully"}, 200

        return {"message": "Food item does not exist"}, 404

    @jwt_required
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

    @jwt_required
    def put(self, food_order_id):
        """ Update the status of an order """

        food_order = FoodOrder().get_by_id(food_order_id)

        if not food_order:
            return {"message": "Food order does not exist"}, 404

        if food_order.status == "pending":
            food_order.status = "approved"

        return food_order.serialize(), 200
