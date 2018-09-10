import os
import psycopg2
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash
from instance import config

try:
    conn = psycopg2.connect(
        host=os.getenv("HOST"), database=os.getenv("DATABASE"),
        user=os.getenv("USER"), password=os.getenv("PASSWORD")
    )
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


class User:

    def __init__(self, username=None, email=None, password=None, is_admin=False):
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def add(self):
        """ Add a user to the user table """
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users(username, email, password, is_admin) VALUES(%s, %s, %s, %s)""",
            (self.username, self.email, self.password_hash, self.is_admin)
        )
        conn.commit()
        cur.close()

    def get_by_id(self, user_id):
        """ get a user by id """
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))

        user = cur.fetchone()

        conn.commit()
        cur.close()

        if not user:
            return None
        return self.map_user(user)

    def get_by_username(self, username):
        """ get user by username """
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))

        user = cur.fetchone()

        conn.commit()
        cur.close()

        if user:
            return self.map_user(user)
        return None

    def get_by_email(self, email):
        """ get user by email """
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))

        user = cur.fetchone()

        conn.commit()
        cur.close()

        if not user:
            return None
        return self.map_user(user)

    def map_user(self, data):
        ''' Map a user to an object '''
        self.id = data[0]
        self.username = data[1]
        self.email = data[2]
        self.password_hash = data[3]
        self.is_admin = data[4]

        return self

    def serialize(self):
        """ serialize a food item to a dictionary """
        return dict(
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            is_admin=self.is_admin
        )


class FoodItem:

    def __init__(self, name=None, description=None, price=None):
        self.name = name
        self.description = description
        self.price = price
        self.date = datetime.now().replace(second=0, microsecond=0)

    def add(self):
        """ Add a fooditem to the fooditems table """
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO fooditems(name, description, price, date) VALUES(%s,%s, %s, %s)""",
            (self.name, self.description, self.price, self.date)
        )
        conn.commit()
        cur.close()

    def get_by_id(self, food_id):
        """ Fetch a food item by its id """
        cur = conn.cursor()
        cur.execute("SELECT * FROM fooditems WHERE id=%s", (food_id,))

        food_item = cur.fetchone()

        conn.commit()
        cur.close()

        if food_item:
            return self.map_fooditem(food_item)
        return None

    def get_all(self):
        """ get all available food items """
        cur = conn.cursor()
        cur.execute("SELECT * FROM fooditems")

        food_items = cur.fetchall()

        conn.commit()
        cur.close()

        if food_items:
            return [self.map_fooditem(food_item) for food_item in food_items]
        return None

    def map_fooditem(self, data):
        ''' Map a user to an object '''
        self.id = data[0]
        self.name = data[1]
        self.description = data[2]
        self.price = data[3]
        self.date = data[4]

        return self

    def serialize(self):
        """ serialize a food item to a dictionary """
        return dict(
            name=self.name,
            description=self.description,
            price=self.price,
            date=str(self.date)
        )


class FoodOrder:

    def __init__(self, name=None, destination=None):
        self.name = name
        self.destination = destination
        self.status = "pending"
        self.date = datetime.now().replace(second=0, microsecond=0)

    def add(self):
        """ Add a foodorder to the foodorders table """
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO foodorders(name, destination, status, date) VALUES(%s,%s, %s, %s)""",
            (self.name, self.destination, self.status, self.date)
        )

        conn.commit()
        cur.close()

    def get_by_id(self, food_order_id):
        """ get a food order by its id """
        cur = conn.cursor()
        cur.execute("SELECT * FROM foodorders WHERE id=%s", (food_order_id,))

        food_order = cur.fetchone()

        conn.commit()
        cur.close()

        if food_order:
            return self.map_foodorder(food_order)
        return None

    def get_all(self):
        """ get all available food orders """
        cur = conn.cursor()
        cur.execute("SELECT * FROM foodorders")

        food_orders = cur.fetchall()

        conn.commit()
        cur.close()

        if food_orders:
            return [self.map_foodorder(food_order) for food_order in food_orders]
        return None

    def map_foodorder(self, data):
        ''' Map a user to an object '''
        self.id = data[0]
        self.name = data[1]
        self.destination = data[2]
        self.status = data[3]
        self.date = data[4]

        return self

    def serialize(self):
        """ serialize a food order to a dictionary """
        return dict(
            name=self.name,
            destination=self.destination,
            status=self.status,
            date=str(self.date)
        )
