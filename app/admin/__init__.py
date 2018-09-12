from flask import Blueprint
from .admim_views import Foods, SpecificOrder, SpecificItem, AcceptOrder, DeclineOrder, CompleteOrder, AcceptedOrders, DeclinedOrders, CompletedOrders

admin_blueprint = Blueprint('admin', __name__)
