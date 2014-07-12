"""
Primary flask blueprint for all primary endpoints.
"""
from flask import Blueprint

main = Blueprint('main', __name__)

# Import the individual endpoints.
from index import *
