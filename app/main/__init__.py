from flask import Blueprint

main = Blueprint("main",__name__)

from . import views 
from . import forms 
from . import errors

