from flask_restful import Resource,reqparse
from models.models import FoodItem, FoodItems

class Foods(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('description', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('price', type=int, required=True, help='This field cannot be left blank')

    def post(self):
        """ Create a new food item """
        request_data = Foods.parser.parse_args()

        name = request_data['name']
        description = request_data['description']
        price = request_data['price']

        food_item = FoodItem(name, description, price)

        FoodItems.append(food_item)

        return {"message":"Food item created successfully"}, 201

    def get(self):
        """ Get all food items """
        return {"Food Items": [food_item.serialize() for food_item in FoodItems]}



