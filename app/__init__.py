from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from instance.config import app_config
from .admin.admim_views import Foods, SpecificOrder, SpecificItem, AcceptOrder, DeclineOrder, CompleteOrder, AcceptedOrders, DeclinedOrders, CompletedOrders


from .customer.customer_views import PostOrders, GetOrders, SpecificCustomerOrders
from .auth.auth_views import Login, SignUp, Logout
# from models.models import Blacklist


jwt = JWTManager()


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    # app.config['JWT_SECRET_KEY'] = 'super-secret'
    # app.config['JWT_BLACKLIST_ENABLED'] = True
    # app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

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

    # @jwt.token_in_blacklist_loader
    # def check_if_token_in_blacklist(token):
    #     ''' Check if token is in blacklist '''
    #     return Blacklist().is_jti_blacklisted(token['jti'])

    admin.add_resource(Foods, '/fooditems')
    admin.add_resource(SpecificOrder, '/fooditems/orders/<int:food_order_id>')
    admin.add_resource(SpecificItem, '/fooditems/<int:food_item_id>')
    admin.add_resource(
        AcceptOrder, '/fooditems/orders/<int:food_order_id>/accept')
    admin.add_resource(
        DeclineOrder, '/fooditems/orders/<int:food_order_id>/decline')
    admin.add_resource(
        CompleteOrder, '/fooditems/orders/<int:food_order_id>/complete')
    admin.add_resource(AcceptedOrders, '/fooditems/orders/accepted')
    admin.add_resource(DeclinedOrders, '/fooditems/orders/declined')
    admin.add_resource(CompletedOrders, '/fooditems/orders/completed')

    auth.add_resource(SignUp, '/signup')
    auth.add_resource(Login, '/login')
    auth.add_resource(Logout, '/logout')

    customer.add_resource(PostOrders, '/<int:food_id>/orders')
    customer.add_resource(GetOrders, '/orders')
    customer.add_resource(SpecificCustomerOrders, '/orders/customer_name')

    return app
