"""
Primary flask blueprint for all primary endpoints.
"""
from flask import Blueprint

main = Blueprint('main', __name__)

# Import the individual endpoints.
from index import *
from verify import *
from import_words import *
from export_words import *
