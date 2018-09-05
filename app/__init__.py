from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from instance.config import app_config
from .admin.admim_views import Foods, SpecificOrder
from .customer.customer_views import PostOrders, GetOrders
from .auth.auth_views import Login, SignUp


jwt = JWTManager()


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    jwt.init_app(app)

    from .admin import admin_blueprint as admin_blp
    admin = Api(admin_blp)
    app.register_blueprint(admin_blp, url_prefix="/api/v1")

    from .auth import auth_blueprint as auth_bp
    auth = Api(auth_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    from .customer import customer_blueprint as customer_bp
    customer = Api(customer_bp)
    app.register_blueprint(customer_bp, url_prefix="/api/v1/fooditems")

    admin.add_resource(Foods, '/fooditems')
    admin.add_resource(SpecificOrder, '/fooditems/orders/<int:food_order_id>')

    auth.add_resource(SignUp, '/signup')
    auth.add_resource(Login, '/login')

    customer.add_resource(PostOrders, '/<int:food_id>/orders')
    customer.add_resource(GetOrders, '/orders')

    return app
