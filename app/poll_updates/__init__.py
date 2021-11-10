from flask import Blueprint
from update_waiter import UpdateWaiter

bp = Blueprint('updates', __name__)
update_waiter = UpdateWaiter()

from app.poll_updates import views
