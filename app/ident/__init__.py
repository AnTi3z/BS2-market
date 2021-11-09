from flask import Blueprint

bp = Blueprint('ident', __name__)

from app.ident import views
