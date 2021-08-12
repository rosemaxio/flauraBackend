from flask import Blueprint

plants = Blueprint('plants', __name__)

from . import Api