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


@app.cli.command()
def create_admin():
    admin = User(username='AdminUser', email='admin@gmail.com',
                 password='pbkdf2:sha256:50000$s3wjDL5p$15bfdf53ba388bb76fdbd0ec5f212abfc10d2731037f1c9716c94945e150d013', is_admin=True)
    admin.add()


if __name__ == '__main__':
    app.run()
