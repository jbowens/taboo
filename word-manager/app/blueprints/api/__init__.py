"""
Primary flask blueprint for all primary endpoints.
"""
from flask import Blueprint

api = Blueprint('api', __name__)

# Import the individual endpoints.
from remove_prohibited import *
from approve import *
from reject import *
from add_prohibited import *
from search import *
