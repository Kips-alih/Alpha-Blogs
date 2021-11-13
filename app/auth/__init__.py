from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views,forms #import registration forms