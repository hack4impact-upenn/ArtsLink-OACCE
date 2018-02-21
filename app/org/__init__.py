from flask import Blueprint

org = Blueprint('org', __name__)

from . import views, errors  # noqa
