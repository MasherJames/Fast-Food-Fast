from datetime import datetime
from werkzeug.security import generate_password_hash

FoodItems = []
FoodOrders = []
users = []


class FoodItem:

    food_item_id = 1

    def __init__(self, name=None, description=None, price=None):
        self.name = name
        self.description = description
        self.price = price
        self.date = datetime.now().replace(second=0, microsecond=0)
        self.id = FoodItem.food_item_id

        FoodItem.food_item_id += 1

    def serialize(self):
        """ serialize a food item to a dictionary """
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            date=str(self.date)
        )

    def get_by_id(self, food_id):
        """ Fetch a food item by its id """
        for food_item in FoodItems:
            if food_item.id == food_id:
                return food_item


class FoodOrder:

    food_order_id = 1

    def __init__(self, name=None, destination=None):
        self.name = name
        self.destination = destination
        self.status = "pending"
        self.date = datetime.now().replace(second=0, microsecond=0)
        self.id = FoodOrder.food_order_id

        FoodOrder.food_order_id += 1

    def get_by_id(self, food_order_id):
        """ get a food order by its id """
        for food_order in FoodOrders:
            if food_order.id == food_order_id:
                return food_order

    def serialize(self):
        """ serialize a food order to a dictionary """
        return dict(
            id=self.id,
            name=self.name,
            destination=self.destination,
            status=self.status,
            date=str(self.date)
        )


class User:

    user_id = 1

    def __init__(self, username=None, email=None, password=None, is_admin=None):
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.id = User.user_id

        User.user_id += 1

    def get_by_id(self, user_id):
        for user in users:
            if user.id == user_id:
                return user

    def get_by_username(self, username):
        for user in users:
            if user.username == username:
                return user

    def get_by_email(self, email):
        for user in users:
            if user.email == email:
                return user

    def serialize(self):
        """ serialize a food item to a dictionary """
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password_hash,
            is_admin=self.is_admin
        )
