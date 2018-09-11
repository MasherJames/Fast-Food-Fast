import os
import click
from app import create_app
from models.models import FastFoodsDb, User, FoodItem, FoodOrder

app = create_app(os.getenv("APP_SETTINGS") or 'default')


@app.cli.command()
def migrate():
    FastFoodsDb().init_app(app)
    User().create_table()
    FoodItem().create_table()
    FoodOrder().create_table()


@app.cli.command()
def drop():
    FastFoodsDb().init_app(app)
    User().drop_table()
    FoodItem().drop_table()
    FoodOrder().drop_table()


if __name__ == '__main__':
    app.run()
