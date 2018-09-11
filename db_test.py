import os
from models.models import FastFoodsDb, User, FoodItem, FoodOrder
from app import create_app

app = create_app("testing")


def migrate():
    FastFoodsDb().init_app(app)
    User().create_table()
    FoodItem().create_table()
    FoodOrder().create_table()


def drop():
    FastFoodsDb().init_app(app)
    User().drop_table()
    FoodItem().drop_table()
    FoodOrder().drop_table()
