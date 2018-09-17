import os
import click
from werkzeug.security import generate_password_hash
from app import create_app
from models.models import FastFoodsDb, User, FoodItem, FoodOrder, Blacklist

app = create_app(os.getenv("APP_SETTINGS") or 'default')


@app.cli.command()
def migrate():
    FastFoodsDb().init_app(app)
    User().create_table()
    FoodItem().create_table()
    FoodOrder().create_table()
    Blacklist().create_table()


@app.cli.command()
def drop():
    FastFoodsDb().init_app(app)
    User().drop_table()
    FoodItem().drop_table()
    FoodOrder().drop_table()
    Blacklist().drop_table()


@app.cli.command()
def create_admin():
    admin = User(username='AdminUser', email='admin@gmail.com',
                 password='Adminpass123', is_admin=True)
    admin.add()


if __name__ == '__main__':
    app.run()
