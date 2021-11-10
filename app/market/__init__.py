from flask import Blueprint
from app.market.cached_dataset import VolDataset

bp = Blueprint('market', __name__)
vol_data = VolDataset()

from app.market import views
