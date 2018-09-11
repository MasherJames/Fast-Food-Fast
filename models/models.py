import os
import psycopg2
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash


class FastFoodsDb:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                current_app.config.get('DATABASE_URL'))

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def init_app(self, app):
        self.conn = psycopg2.connect(app.config.get('DATABASE_URL'))


class User(FastFoodsDb):

    def __init__(self, username=None, email=None, password=None, is_admin=False):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            '''
            CREATE TABLE users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE,
                email VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL,
                is_admin BOOLEAN NOT NULL
            )
        '''
        )
        self.conn.commit()
        cur.close()

    def drop_table(self):
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS users')
        self.conn.commit()
        cur.close()

    def add(self):
        """ Add a user to the user table """
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO users(username, email, password, is_admin) VALUES(%s, %s, %s, %s)""",
            (self.username, self.email, self.password_hash, self.is_admin)
        )
        self.conn.commit()
        cur.close()

    def get_by_id(self, user_id):
        """ get a user by id """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))

        user = cur.fetchone()

        self.conn.commit()
        cur.close()

        if not user:
            return None
        return self.map_user(user)

    def get_by_username(self, username):
        """ get user by username """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))

        user = cur.fetchone()

        self.conn.commit()
        cur.close()

        if user:
            return self.map_user(user)
        return None

    def get_by_email(self, email):
        """ get user by email """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))

        user = cur.fetchone()

        self.conn.commit()
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
            id=self.id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            is_admin=self.is_admin
        )


class FoodItem(FastFoodsDb):

    def __init__(self, name=None, description=None, price=None):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.date = datetime.now().replace(second=0, microsecond=0)

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            '''
            CREATE TABLE fooditems(
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL ,
                description VARCHAR NOT NULL,
                price INTEGER NOT NULL,
                date TIMESTAMP
            )
        '''
        )
        self.conn.commit()
        cur.close()

    def drop_table(self):
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS fooditems')
        self.conn.commit()
        cur.close()

    def add(self):
        """ Add a fooditem to the fooditems table """
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO fooditems(name, description, price, date) VALUES(%s,%s, %s, %s)""",
            (self.name, self.description, self.price, self.date)
        )
        self.conn.commit()
        cur.close()

    def get_by_id(self, food_id):
        """ Fetch a food item by its id """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM fooditems WHERE id=%s", (food_id,))

        food_item = cur.fetchone()

        self.conn.commit()
        cur.close()

        if food_item:
            return self.map_fooditem(food_item)
        return None

    def get_all(self):
        """ get all available food items """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM fooditems")

        food_items = cur.fetchall()

        self.conn.commit()
        cur.close()

        if food_items:
            return [self.map_fooditem(food_item) for food_item in food_items]
        return None

    def map_fooditem(self, data):
        ''' Map a user to an object '''
        item = FoodItem(name=data[1], description=data[2], price=data[3])
        item.id = data[0]
        item.date = data[4]
        self = item
        return self

    def serialize(self):
        """ serialize a food item to a dictionary """
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            date=str(self.date)
        )


class FoodOrder(FastFoodsDb):

    def __init__(self, ordered_by=None, order_name=None, destination=None):
        super().__init__()
        self.ordered_by = ordered_by
        self.order_name = order_name
        self.destination = destination
        self.status = "pending"
        self.date = datetime.now().replace(second=0, microsecond=0)

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            '''
            CREATE TABLE foodorders(
                id serial PRIMARY KEY,
                ordered_by VARCHAR NOT NULL,
                order_name VARCHAR NOT NULL,
                destination VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                date TIMESTAMP
            )
            '''
        )
        self.conn.commit()
        cur.close()

    def drop_table(self):
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS foodorders')
        self.conn.commit()
        cur.close()

    def add(self):
        """ Add a foodorder to the foodorders table """
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO foodorders(ordered_by, order_name, destination, status, date)
            VALUES(%s, %s, %s, %s, %s)
            """,
            (self.ordered_by, self.order_name,
             self.destination, self.status, self.date)
        )

        self.conn.commit()
        cur.close()

    def get_by_id(self, food_order_id):
        """ get a food order by its id """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM foodorders WHERE id=%s", (food_order_id,))

        food_order = cur.fetchone()

        self.conn.commit()
        cur.close()

        if food_order:
            return self.map_foodorder(food_order)
        return None

    def get_by_requester(self, requester):
        """ Get by ordered by... """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM foodorders WHERE ordered_by=%s",
                    (requester,))

        food_orders = cur.fetchall()

        self.conn.commit()
        cur.close()

        if food_orders:
            return [self.map_foodorder(food_order) for food_order in food_orders]
        return None

    def get_all(self):
        """ get all available food orders """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM foodorders")

        food_orders = cur.fetchall()

        self.conn.commit()
        cur.close()

        if food_orders:
            return [self.map_foodorder(food_order) for food_order in food_orders]
        return None

    def map_foodorder(self, data):
        ''' Map a user to an object '''
        order = FoodOrder(
            ordered_by=data[1], order_name=data[2], destination=data[3])
        order.id = data[0]
        order.status = data[4]
        order.date = data[5]
        self = order

        return self

    def serialize(self):
        """ serialize a food order to a dictionary """
        return dict(
            id=self.id,
            ordered_by=self.ordered_by,
            order_name=self.order_name,
            destination=self.destination,
            status=self.status,
            date=str(self.date)
        )
