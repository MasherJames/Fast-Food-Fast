from flask import Blueprint
from .admim_views import Foods, SpecificOrder

admin_blueprint = Blueprint('admin', __name__)