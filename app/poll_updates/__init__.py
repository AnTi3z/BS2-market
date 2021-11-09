from flask import Blueprint

bp = Blueprint('updates', __name__)

from app.poll_updates import views
