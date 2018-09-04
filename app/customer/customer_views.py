from flask_restful import Resource,reqparse
from models.models import FoodOrder, FoodOrders, FoodItem

class PostOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('destination', type=str, required=True, help='This field cannot be left blank')

    def post(self, food_id):
        """ Place an order for a specific food item"""
        request_data =  PostOrders.parser.parse_args()

        destination = request_data['destination']

        food_item =  FoodItem().get_by_id(food_id)
        if not food_item:
            return {"message":"Food item does not exist"}, 404

        food_order = FoodOrder(food_item.name, destination)
        FoodOrders.append(food_order)

        return {"message":"Food order placed succssesfully"}, 201

class GetOrders(Resource):

    def get(self):
        """ get all the orders """
        return{"Food orders": [food_order.serialize() for food_order in FoodOrders]}