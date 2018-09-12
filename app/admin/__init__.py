from flask import Blueprint
from .admim_views import Foods, SpecificOrder, SpecificItem

admin_blueprint = Blueprint('admin', __name__)
