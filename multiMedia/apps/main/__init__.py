from flask import Blueprint

main = Blueprint('main',__name__)

from apps.main import views,forms